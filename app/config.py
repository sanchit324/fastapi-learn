from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str  
    access_token_expire_minutes: int  # Changed from access_token_expiration_time

    model_config = {
        "env_file": ".env"
    }

settings = Settings()