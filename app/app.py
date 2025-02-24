from fastapi import FastAPI, HTTPException, status

from task_worker.db_worker.db_redis import DbRedis
from task_worker.task_worker import TaskWorker
from schemas.task import StatusResponse, CreateTaskResponse
from settings import REDIS_SETTINGS


app = FastAPI()
app.add_event_handler("startup", lambda: startup_event())


def startup_event():
    global task_worker
    redis_client = DbRedis(
        host=REDIS_SETTINGS.redis_host,
        port=REDIS_SETTINGS.redis_port,
        db=REDIS_SETTINGS.redis_db,
    )  # TODO: make changable
    task_worker = TaskWorker(redis_client)


@app.post(
    "/create_task",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateTaskResponse,
    description="Creates task and return it's id",
)
async def create_task() -> int:
    task_id = await task_worker.create_task()
    return CreateTaskResponse(task_id=task_id)


@app.get(
    "/task/{task_id}",
    response_model_exclude_unset=True,
    response_model=StatusResponse,
    responses={
        404: {"description": "Task not found"},
    },
    description="Returns task by id",
)
async def get_task(task_id: int) -> StatusResponse:
    task = await task_worker.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return StatusResponse(**task)
