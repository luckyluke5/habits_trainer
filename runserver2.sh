#!/bin/bash

python3 -m poetry install
pip install psycopg2
pip install psycopg2-binary
python manage.py runserver 0.0.0.0:3000