from enum import Enum
from pydantic_settings import BaseSettings


class TestState(str, Enum):
    TRUE = "1"
    FALSE = "0"


class Settings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_db: int
    is_testing: TestState = TestState.FALSE

    class Config:
        env_file = ".env"


REDIS_SETTINGS = Settings()
TASK_EMOUNT = 2
