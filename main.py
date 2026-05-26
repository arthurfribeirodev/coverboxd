from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI()

# Instalar Argon2
bcrypt_context = CryptContext(schemes=["argon2"], deprecated="auto")

from auth_routes import auth_router
from reviews_routes import review_router

app.include_router(auth_router)
app.include_router(review_router)