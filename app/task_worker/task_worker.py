import asyncio
from datetime import datetime
from random import randint

from task_worker.statuses import Statuses
from .db_worker.db_base import DbBase
from settings import TASK_EMOUNT
import logging


class TaskWorker:
    def __init__(self, task_db: DbBase):
        self._task_db: DbBase = task_db
        self._semaphore = asyncio.Semaphore(TASK_EMOUNT)
        self._running_tasks: dict[int, asyncio.Task] = {}

    async def create_task(self) -> int:
        task_id = await self._task_db.create_task()
        asyncio.create_task(self._execute_task(task_id))
        logging.info(f"Task {task_id} created")
        return task_id

    async def get_task(self, task_id: int) -> dict:
        return await self._task_db.get_task(task_id)

    async def get_queued_tasks(self) -> list[dict]:
        return await self._task_db.get_queued_tasks()

    async def _execute_task(self, task_id: int):
        async with self._semaphore:
            task = await self.get_task(task_id)
            start_time = datetime.now()
            dict_to_update = {
                "status": Statuses.RUN,
                "start_time": start_time.isoformat(),
                "create_time": task["create_time"],
            }
            await self._task_db.update_task(task_id, dict_to_update)
            # Имитация выполнения задачи
            execution_time = randint(0, 10)
            await asyncio.sleep(execution_time)
            # Обновляем статус задачи на "Completed"
            dict_to_update["time_to_execute"] = (
                datetime.now() - start_time
            ).total_seconds()
            dict_to_update["status"] = Statuses.COMPLETED
            await self._task_db.update_task(task_id, dict_to_update)
            logging.info(f"Task {task_id} completed in {execution_time} seconds")
