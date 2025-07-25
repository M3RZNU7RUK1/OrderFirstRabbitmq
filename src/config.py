from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str  
    DB_PORT: int  
    DB_USER: str 
    DB_PASS: str  
    DB_NAME: str 
    JWT_SECRET_KEY: str
    USERNAME_ADMIN: str
    PASSWORD_ADMIN: str
    PHONE_NUMBER_ADMIN: str
    TOKEN: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DB: int
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8"  
    )

settings = Settings()
