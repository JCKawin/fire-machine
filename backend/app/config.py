from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Fire Machine API"
    app_version: str = "0.1.0"
    debug: bool = False

    influx_url: str = "http://localhost:8086"
    influx_org: str = "fire-machine"
    influx_bucket: str = "sensors"
    influx_token: str = "fire-machine-super-secret-token"

    ai_model_path: str = "./models"
    cors_origins: str = "http://localhost:5173,http://localhost:3001"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
