from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DATABASE_URL: str
    JWT_SECRETE: str
    JWT_ALGO: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


Config = Setting()
