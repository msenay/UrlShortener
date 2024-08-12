from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App settings."""

    # app miscellanea
    app_host: str = "0.0.0.0"
    app_port: int = 8001
    log_level: str = "INFO"

    # postgres
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    main_db_url: str = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}"
    db_url: str = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

    # redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_url: str = f"redis://{redis_host}:{redis_port}"


settings = Settings()
