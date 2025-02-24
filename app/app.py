from fastapi import Depends, FastAPI, HTTPException, status
from settings import REDIS_SETTINGS
from task_worker.task_worker import TaskWorker
from schemas.task import StatusResponse, CreateTaskResponse
from task_worker.db_worker.db_redis import DbRedis

app = FastAPI()


def get_redis_client():
    redis_client = DbRedis(
        host=REDIS_SETTINGS.redis_host,
        port=REDIS_SETTINGS.redis_port,
        db=REDIS_SETTINGS.redis_db,
        is_testing=REDIS_SETTINGS.is_testing,
    )
    return redis_client


def get_task_worker():
    redis_client = get_redis_client()
    return TaskWorker(redis_client)


@app.post(
    "/create_task",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateTaskResponse,
    description="Creates task and return it's id",
)
async def create_task(
    task_worker: TaskWorker = Depends(get_task_worker),
) -> CreateTaskResponse:
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
async def get_task(
    task_id: int, task_worker: TaskWorker = Depends(get_task_worker)
) -> StatusResponse:
    task = await task_worker.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return StatusResponse(**task)
