#!/bin/bash

python3 -m poetry install
python manage.py runserver 0.0.0.0:3000