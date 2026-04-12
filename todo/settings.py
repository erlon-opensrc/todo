from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Carrega as variáveis em um arquivo de configuração
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )

    # valores fornecidos por .env
    DATABASE_URL: str = Field(init=False)
    SECRET_KEY: str = Field(init=False)
    ALGORITHM: str = Field(init=False)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(init=False)
