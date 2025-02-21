from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int

    class Config:
        env_file = ".env"


REDIS_SETTINGS = Settings()
TASK_EMOUNT = 2
