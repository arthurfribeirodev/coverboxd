from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


load_dotenv()

    # Utilização das variáveis de ambiente para criptografia de senha e JWT

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI()


    # CORS configurado para permitir requisições de qualquer origem, dividindo front e backend
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    # Criptografia de Senha e OAuth2
bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_schme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    # Importação das rotas de autenticação, reviews e álbuns, e inclusão no aplicativo FastAPI

from auth_routes import auth_router
from reviews_routes import review_router
from albuns_routes import albuns_router

app.include_router(auth_router)
app.include_router(review_router)
app.include_router(albuns_router)