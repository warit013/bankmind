from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"
    database_url: str = "postgresql://bankmind:bankmind@localhost:5432/bankmind"
    llm_provider: str = "ollama"  # ollama | openai
    llm_model: str = "qwen2.5:7b"
    llm_api_key: str = ""
    ollama_url: str = "http://localhost:11434"
    top_k: int = 3


settings = Settings()