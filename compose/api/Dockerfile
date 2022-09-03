FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY app .

CMD python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload
