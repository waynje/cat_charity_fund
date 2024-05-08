from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Charity Project'
    app_description: str = 'Приложение для  фонда поддержки котиков QRKot.'
    database_url: str = 'sqlite+aiosqlite:///./charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()