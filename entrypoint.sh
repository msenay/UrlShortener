#!/bin/bash
set -ex

python3 -c "from app.database.crud import init_db; init_db()"

python3 app/main.py
