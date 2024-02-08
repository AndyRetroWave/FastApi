FROM python:3.11

RUN mkdir /booking

WORKDIR /booking

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]