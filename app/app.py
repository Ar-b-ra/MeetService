from fastapi import FastAPI
from schemas.task import StatusResponse


app = FastAPI()


@app.post("/create_task", description="Creates task and return it's id")
async def create_task() -> int:
    return {"message": "New task created"}


@app.get("/get_task/{task_id}", response_model=StatusResponse, description="Returns task by id")
async def get_task(task_id: int) -> int:
    return {"message": f"Task id: {task_id}"}
