from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Easy Read Adapter"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    api_key: str = ""
    database_path: str = "./data/easy_read.db"
    debug: bool = False
    public_base_url: str = "http://localhost:8000"
    pictogram_providers: str = "own,mulberry,openmoji"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
