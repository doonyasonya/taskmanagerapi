# Task Manager (FastAPI)

Простой Task Manager с CRUD-операциями для задач, проверкой статусов и тестами на **pytest** и **Gauge**.

---

##  Запуск локально

1. Клонируй репозиторий:
```bash
git clone https://github.com/doonyasonya/task-manager-fastapi.git
cd task-manager-fastapi
```
2. Создай виртуальное окружение и активируй его:
```bash
python -m venv .venv
source .venv/bin/activate   # для Linux/Mac
source .venv/Scripts/activate      # для Windows
```
3. Установи зависимости:
```bash
pip install -r requirements.txt
```
4. Запусти сервер:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
5. Проверь API:
Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc


---

## Запуск через Docker

1. Собери Docker-образ:
```bash
docker build -t task-manager .
```
2. Запусти контейнер:
```bash
docker run -p 8000:8000 task-manager
```
---
## Тесты
1. Pytest
```bash
pytest tests/test_main.py
```
2. Gauge
```bash
gauge run tests/specs/
```
