from datetime import datetime
from .db_base import DbBase
from redis import Redis
from task_worker.statuses import Statuses


class DbRedis(DbBase):
    def __init__(self, host, port, db):
        self._client: Redis = Redis(host=host, port=port, db=db, decode_responses=True)

    async def get_task(self, task_id):
        return await self._client.get(f"task:{task_id}")

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
        self._client.rpush("task_queue", task_id)

        return task_id

    async def update_task(self, task_id: int):
        pass