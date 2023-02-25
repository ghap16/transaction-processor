from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    BUCKET: str
    EMAIL_FROM: EmailStr
    EMAIL_TO: EmailStr
    TMP_PATH: str = "/tmp/"
    REGION_NAME: str = "us-east-1"
    PREFIX_FILE: str = "account"
    DECIMAL_PRECISION: int = 2
    DEBUG: bool = True


settings = Settings()
