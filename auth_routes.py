from fastapi import APIRouter, Depends, HTTPException
from models import Users,db
from dependencies import session_grab,verify_token
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACESS_TOKEN_EXPIRE_MINUTES
from schemas import UserSchema, loginSchema
from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone 


auth_router = APIRouter(prefix="/auth",tags=["auth"])


def  token_gen(id, duration_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):
    expire_date= datetime.now(timezone.utc) + duration_token
    dic_info = {"sub": str(id), "exp": expire_date}
    token = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return token




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
    
@auth_router.post("/login")
async def login(login_schema: loginSchema, session = Depends(session_grab)):
    usuario = session.query(Users).filter(Users.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Email inexistente")
    elif not bcrypt_context.verify(login_schema.senha, usuario.senha):
        raise HTTPException(status_code=400, detail="Senha incorreta")
    else:
        acess_token = token_gen(usuario.id)
        refresh_token = token_gen(usuario.id, duration_token=timedelta(days=7))
        return {
            "acess_token": acess_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": usuario.id
            }
    
@auth_router.get("/refresh")
async def refresh_token(user: Users = Depends(verify_token)):
    acess_token = token_gen(user.id)
    return {
            "acess_token": acess_token, 
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id        
            }