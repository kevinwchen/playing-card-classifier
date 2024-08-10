FROM python:3.11.9-bullseye

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./api /app/api

ENV PYTHONPATH=/app/api

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]