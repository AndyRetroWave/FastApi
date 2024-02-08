#!/bin/bash

if [[ "${1}" == "celery" ]]; then
    pip install -U "celery[redis]"
    celery --app=app.tasks.celery:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
    celery --app=app.tasks.celery:celery flower
fi    