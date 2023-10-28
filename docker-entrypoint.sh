#!/usr/bin/env bash

# Wait for postgres to start
/wait

alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 80
