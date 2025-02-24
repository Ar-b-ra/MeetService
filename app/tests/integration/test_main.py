from datetime import datetime
from fastapi import status


def test_create_task(test_client, fake_redis):
    response = test_client.post("/create_task")
    assert response.status_code == status.HTTP_201_CREATED
    assert "task_id" in response.json()

    # Проверяем, что задача добавлена в Redis
    task_id = response.json()["task_id"]
    task_data = fake_redis.hgetall(f"task:{task_id}")
    assert task_data is not None


def test_get_task_status(test_client):
    # Создаем задачу
    create_response = test_client.post("/create_task")
    task_id = create_response.json()["task_id"]

    # Получаем статус задачи
    status_response = test_client.get(f"/task_status/{task_id}")
    assert status_response.status_code == status.HTTP_200_OK

    # Проверяем поля в ответе
    status_data = status_response.json()
    assert status_data["status"] == "In Queue"
    assert status_data["create_time"] is not None
    assert status_data["start_time"] == "Not started"
    assert status_data["time_to_execute"] == 0


def test_get_task_status_not_found(test_client):
    response = test_client.get("/task_status/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_task_execution(test_client, fake_redis):
    # Создаем задачу
    create_response = test_client.post("/create_task")
    task_id = create_response.json()["task_id"]

    # Имитируем выполнение задачи
    fake_redis.hset(f"task:{task_id}", "status", "Run")
    fake_redis.hset(f"task:{task_id}", "start_time", datetime.now().isoformat())
    fake_redis.hset(f"task:{task_id}", "exec_time", 5)

    # Получаем статус задачи
    status_response = test_client.get(f"/task_status/{task_id}")
    assert status_response.status_code == status.HTTP_200_OK

    # Проверяем поля в ответе
    status_data = status_response.json()
    assert status_data["status"] == "Run"
    assert status_data["start_time"] is not None
    assert status_data["time_to_execute"] == 5
