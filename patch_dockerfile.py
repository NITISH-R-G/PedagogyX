import sys
content = open('services/worker-metrics/Dockerfile').read()
content = content.replace('CMD ["python", "-m", "worker.main"]', 'CMD ["python", "-m", "worker.metrics_main"]')
with open('services/worker-metrics/Dockerfile', 'w') as f:
    f.write(content)
