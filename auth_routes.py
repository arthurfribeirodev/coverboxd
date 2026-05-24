from fastapi import APIRouter, Depends
from models import Users,db
from dependencies import session_grab

auth_router = APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/register")
async def register(username: str, email: str, senha: str, session = Depends(session_grab)):

    user = session.query(Users).filter(email==email).first()
    if user:
        return {"message": "Email já registrado"}
    else:
        new_user = Users(username, email, senha)
        session.add(new_user)
        session.commit()
        return {"message": "Usuário registrado com sucesso"}