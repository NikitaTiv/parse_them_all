import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = '5432'
    TESSERACT_URL: str = 'http://tesseract-api:8001'

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

    @property
    def database_dict(self) -> str:
        return {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': self.POSTGRES_DB,
            'USER': self.POSTGRES_USER,
            'PASSWORD': self.POSTGRES_PASSWORD,
            'HOST': self.POSTGRES_HOST,
            'PORT': self.POSTGRES_PORT,
        }


settings = Settings()
