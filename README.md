# FastAPI Task Manager


A simple task manager to implement a Kanban Board


The technology stack used for this application is as follows:

- Framework
    - FastAPI and Starlette (A lightweight ASGI framework/toolkit, which is ideal for building async web services in Python. FastAPI is built on top of starlette)
- ASGI Server
    - Uvicorn and Gunicorn
- Containerization
    - Docker
- Database
    - Postgres
    - Alembic
    - [encode/databases](https://www.encode.io/databases/)
- Authentication
    - Bcrypt
    - Passlib
    - JWT Tokens with Pyjwt
- Testing
    - Pytest
- Development
    - flake8
    - black

## Commands

### Bootstrapping the application
- docker-compose up -d --build

### Run
- docker-compose up

### Check running containers
- docker ps

### Execute bash commands from container interactively
- docker exec -it [CONTAINER_ID] bash

### Run migrations inside the container's shell
- alembic revision -m "message"

## Local URLs

### API Docs
- http://localhost:8000/docs

### PGAdmin:
- http://localhost:5050/

## DB

## Run DB locally
- docker-compose exec db psql -h localhost -U postgres --dbname=postgres
- Try a few commands:
  - \l - list all databases
  - \d+ - list all tables (relations) in the current database
  - \c postgres - connect to the postgres database
  - \d table_name - describe any table and the associated columns

## Tests

### Run tests within the running server container
- docker ps
- docker exec -it [CONTAINER_ID] bash
- pytest -v