from fastapi import HTTPException
import jwt
from datetime import timedelta
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from authx import AuthXConfig, AuthX
from cryptography.fernet import Fernet

load_dotenv()

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
config.JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)

auth = AuthX(config=config)

class Security:
    def __init__(self):
        self.__pwd_context = CryptContext(schemes=["argon2"])
        self.cipher = Fernet(os.getenv("ENCRYPTION_KEY"))
    def decode_token(self, token: bytes):
        try:
            unverified_header = jwt.get_unverified_header(token)
            algorithm = unverified_header.get("alg", "HS256")
            
            payload = jwt.decode(
                token,
                key=os.getenv("JWT_SECRET_KEY"),  # Ваш секретный ключ
                algorithms=[algorithm],
                options={"verify_exp": True}  # Проверяем срок действия
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, token: bytes) -> str:
        return self.cipher.decrypt(token).decode()
    
    def verify(self, hashed_obj, obj):
        return self.__pwd_context.verify(secret=obj, hash=hashed_obj, scheme="argon2")
    
    def hash(self, obj):
        return self.__pwd_context.hash(obj)
    
    def create_jwt(self, user_id: int, user_role: str):
        access_token = auth.create_access_token(uid=str(user_id), data={"role": user_role}) 
        refresh_token = auth.create_refresh_token(uid=str(user_id), data={"role": user_role})
        return access_token, refresh_token
