from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Приложение для фонда поддержки котов.'
    database_url: str = 'sqlite+aiosqlite:///./cat_charity_fund.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    email: Optional[str] = None

    DRIVE_VERSION = 'v3'
    SPREADSHEETS_VERSION = 'v4'
    ROW_COUNT = 100
    COLUMN_COUNT = 11
    FORMAT = '%Y/%m/%d %H:%M:%S'
    TITLE = 'Отчет от: '

    class Config:
        env_file = '.env'


settings = Settings()
