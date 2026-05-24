from fastapi import APIRouter, Depends
from models import Users,db
from dependencies import session_grab
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/register")
async def register(username: str, email: str, senha: str, session = Depends(session_grab)):

    user = session.query(Users).filter(email==email).first()
    if user:
        return {"message": "Email já registrado"}
    else:
        pass_hash = bcrypt_context.hash(senha)
        new_user = Users(username, email, pass_hash)
        session.add(new_user)
        session.commit()
        return {"message": "Usuário registrado com sucesso"}