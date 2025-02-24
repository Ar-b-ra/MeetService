from datetime import datetime
from pydantic import BaseModel, Field
from task_worker.statuses import Statuses


class StatusResponse(BaseModel):
    status: Statuses = Field(description="Статус задачи")
    create_time: datetime = Field(description="Время создания задачи")
    start_time: datetime | None = Field(
        description="Время старта задачи",
        default=None,
    )
    time_to_execute: int | float | None = Field(
        description="Время выполнения задачи",
        default=None,
    )


class CreateTaskResponse(BaseModel):
    task_id: int = Field(
        description="Id созданной задачи",
    )
