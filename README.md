[![codecov](https://codecov.io/gh/Ar-b-ra/MeetService/branch/master/graph/badge.svg)](https://codecov.io/gh/Ar-b-ra/MeetService/)

# Тестовое задание

Необходимо реализовать прототип веб-сервиса по организации очереди задач. Допускается описать труднореализуемые или непонятные моменты алгоритмически.

## Требования к прототипу

1. **API-endpoint для создания задачи**:
   - При обращении к этому эндпоинту создается задача, которая добавляется в очередь.
   - Пользователю возвращается номер задачи.

2. **API-endpoint для получения статуса задачи**:
   - Возвращает статус задачи в формате JSON:
```json
     {
       "status": "...",
       "create_time": "...",
       "start_time": "...",
       "time_to_execute": "..."
     }
```
   - Статусы задачи:
     - `In Queue` — задача ждет своей очереди на выполнение;
     - `Run` — задача запущена;
     - `Completed` — задача выполнена.

4. **Выполнение задачи**:
   - Реализовать в виде заглушки с помощью Python-кода:
```python
time.sleep(random.randint(0, 10))
```
4. **Ограничения**:
   - Можно создавать множество задач, но одновременно должно выполняться не более 2 (двух) задач.

5. **Хранение результатов**:
   - Записать результаты в локальную БД с полями:
     - `id` (первичный ключ, номер поставленной задачи)
     - `create_time` (время создания задачи)
     - `start_time` (время старта задачи)
     - `exec_time` (время выполнения задачи)

6. **Технические ограничения**:
   - Нельзя использовать Celery, Dramatiq, Taskiq и другие готовые фреймворки для работы с очередями задач.
   - При написании использовать Python версии 3.7 и выше.
   - БД на ваше усмотрение.
   - Предпочтительно использовать асинхронный веб-фреймворк.