from datetime import datetime
from fastapi import status
from task_worker.statuses import Statuses


def test_create_task(test_client, fake_redis):
    response = test_client.post("/create_task")
    assert response.status_code == status.HTTP_201_CREATED
    assert "task_id" in response.json()

    # Проверяем, что задача добавлена в Redis
    task_id = response.json()["task_id"]
    task_data = fake_redis.hgetall(f"task:{task_id}")
    assert task_data is not None


def test_get_task_status(test_client, fake_redis):
    task_id = 1
    create_time = datetime.now().isoformat()
    fake_redis.hset(
        f"task:{task_id}",
        mapping={
            "create_time": create_time,
            "status": Statuses.IN_QUEUE,
        },
    )
    status_response = test_client.get(f"/task/{task_id}/")
    assert status_response.status_code == status.HTTP_200_OK
    status_data = status_response.json()
    assert status_data["status"] == Statuses.IN_QUEUE


def test_get_task_status_not_found(test_client):
    response = test_client.get("/task/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
