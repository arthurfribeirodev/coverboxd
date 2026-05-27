from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from dotenv import load_dotenv
import os


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instalar Argon2
bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_schme = OAuth2PasswordBearer(tokenUrl="/auth/login")

from auth_routes import auth_router
from reviews_routes import review_router
from albuns_routes import albuns_router

app.include_router(auth_router)
app.include_router(review_router)
app.include_router(albuns_router)