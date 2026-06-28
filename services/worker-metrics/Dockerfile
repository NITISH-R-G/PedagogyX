FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY worker_metrics ./worker_metrics

CMD ["python", "-m", "worker_metrics.metrics_main"]
