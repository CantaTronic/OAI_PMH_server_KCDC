
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_URL: str = 'https://example.com'
    REPOSITORY_NAME: str = 'Some name'
    ADMIN_EMAIL: str = 'admin@email.com'
    EARLIEST_DATE_TIMESTAMP: str = '2020-01-01T00:00:00Z'
    model_config = SettingsConfigDict(env_file=".env")

config = Settings()
