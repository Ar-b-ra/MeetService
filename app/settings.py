from enum import Enum
from pydantic_settings import BaseSettings


class TestState(str, Enum):
    TRUE = "1"
    FALSE = "0"


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    is_testing: TestState = TestState.FALSE

    class ConfigDict:
        env_file = ".env"


REDIS_SETTINGS = Settings()
TASK_EMOUNT = 2
