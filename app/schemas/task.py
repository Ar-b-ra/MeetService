from datetime import datetime
from pydantic import BaseModel, Field
from task_worker.statuses import Statuses


class StatusResponse(BaseModel):
    status: Statuses = Field(description="Статус задачи")
    create_time: datetime = Field(description="Время создания задачи")
    start_time: datetime | None = Field(
        description="Время старта задачи (может быть None, если задача ещё не началась)"
    )
    time_to_execute: int | None = Field(
        description="Время выполнения задачи (может быть None, если задача ещё не завершена)"
    )
