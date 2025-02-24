import abc


class DbBase(abc.ABC):
    @abc.abstractmethod
    async def create_task(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_task(self, task_id: int) -> int | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_task(self, task_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_queued_tasks(self) -> list[dict]:
        raise NotImplementedError
