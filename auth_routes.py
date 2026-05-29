from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import Users,db
from dependencies import session_grab,verify_token
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES
from schemas import UserSchema, loginSchema
from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone 


auth_router = APIRouter(prefix="/auth",tags=["auth"])


    # Geração do token JWT para autenticação

def  token_gen(id, duration_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expire_date= datetime.now(timezone.utc) + duration_token
    dic_info = {"sub": str(id), "exp": expire_date}
    token = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return token
def authenticate_user(email: str, senha: str, session):
    user = session.query(Users).filter(Users.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(senha, user.senha):
        return False
    return user



    # Metodo POST de registro, com verificação de email já registrado e hash de senha utilizando Argon2
@auth_router.post("/register")
async def register(user_schema: UserSchema, session = Depends(session_grab)):

    user = session.query(Users).filter(Users.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    else:
        pass_hash = bcrypt_context.hash(user_schema.senha)
        new_user = Users(user_schema.username, user_schema.email, pass_hash)
        session.add(new_user)
        session.commit()
        return {"message": f"O email {user_schema.email} foi registrado com sucesso!"}
    

    # Metodo POST de login, com verificação de email e senha, e geração de token JWT para autenticação
@auth_router.post("/login")
async def login(login_schema: loginSchema, session = Depends(session_grab)):
    usuario = authenticate_user(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou Senha incorretos")
    else:
        acess_token = token_gen(usuario.id)
        refresh_token = token_gen(usuario.id, duration_token=timedelta(days=7))
        return {
            "access_token": acess_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": usuario.id
            }
    
@auth_router.post("/login-form")
async def login_form(dados: OAuth2PasswordRequestForm = Depends(), session = Depends(session_grab)):
    user = authenticate_user(dados.username, dados.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    else:
        acess_token = token_gen(user.id)
        return {
            "access_token" : acess_token,
            "token_type": "bearer"
        }
    

    # Geração do Refresh Token 
@auth_router.get("/refresh")
async def refresh_token(user: Users = Depends(verify_token)):
    acess_token = token_gen(user.id)
    return {
            "acess_token": acess_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id        
            }