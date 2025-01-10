from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    DATABASE_URL: str
    JWT_SECRETE: str
    JWT_ALGO: str
    CLOUD_NAME: str
    CLOUDNARY_API_KEY: str
    CLOUDNARY_API_SECRET: str
    MAIL_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


Config = Setting()
