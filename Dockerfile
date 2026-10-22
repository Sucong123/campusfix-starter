FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1
EXPOSE 5000

CMD ["python", "docker-entrypoint.py"]
