# FastAPI Task Manager


A simple task manager to implement a Kanban Board


The technology stack used for this application is as follows:

- Framework
    - FastAPI and Starlette
- ASGI Server
    - Uvicorn and Gunicorn
- Containerization
    - Docker
- Database
    - Postgres
    - Alembic
    - encode/databases
- Authentication
    - Bcrypt
    - Passlib
    - JWT Tokens with Pyjwt
- Testing
    - Pytest
- Development
    - flake8
    - black
    - vscode

## Commands

### Bootstrapping the application
- docker-compose up -d --build

### Run
- docker-compose up

### Check running containers
- docker ps

### Execute bash commands from container interactively
- docker exec -it container_id bash

### Run migrations inside the container's shell
- alembic revision -m "message"

## Local URLs

### API Docs
- http://localhost:8000/docs

### PGAdmin:
- http://localhost:5050/

