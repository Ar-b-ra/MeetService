from datetime import datetime
from fakeredis import FakeRedis

from settings import TestState
from .db_base import DbBase
from redis import Redis
from task_worker.statuses import Statuses


class DbRedis(DbBase):
    def __init__(self, host, port, db, *, is_testing: False):
        if is_testing == TestState.FALSE:
            self._client: Redis = Redis(
                host=host, port=port, db=db, decode_responses=True
            )
        else:
            self._client = FakeRedis()

    async def get_task(self, task_id):
        return self._client.hgetall(f"task:{task_id}")

    async def create_task(self):
        create_time = datetime.now().isoformat()
        task_id = self._client.incr("task_counter")
        self._client.hset(
            f"task:{task_id}",
            mapping={
                "create_time": create_time,
                "status": Statuses.IN_QUEUE,
            },
        )
        return task_id

    async def get_queued_tasks(self):
        queued_tasks = []
        async for task_id in self._client.smembers("task"):
            task = await self.get_task(task_id)
            if task["status"] == Statuses.IN_QUEUE:
                queued_tasks.append(task)
        return queued_tasks

    async def update_task(self, task_id: int, data_to_update: dict):
        task = await self.get_task(task_id)
        if task is None:
            raise ValueError(f"Task with id {task_id} not found")
        task.update(data_to_update)
        self._client.hset(f"task:{task_id}", mapping=task)
