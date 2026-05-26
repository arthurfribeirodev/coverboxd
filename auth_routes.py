from fastapi import APIRouter, Depends, HTTPException
from models import Users,db
from dependencies import session_grab
from main import bcrypt_context
from schemas import UserSchema, loginSchema

auth_router = APIRouter(prefix="/auth",tags=["auth"])


def  token_gen(id):
    token = f"ekwqmkemkwqmkeqw{id}"
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
    if not bcrypt_context.verify(login_schema.senha, usuario.senha):
        raise HTTPException(status_code=400, detail="Senha incorreta")
    else:
        acess_token = token_gen(usuario.id)
        return {"acess_token": acess_token, "token_type": "bearer", "user_id": usuario.id}
