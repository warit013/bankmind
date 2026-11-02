from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    database_url: str = "postgresql://bankmind:bankmind@localhost:5432/bankmind"
    llm_provider: str = "openai"
    llm_api_key: str = ""


settings = Settings()