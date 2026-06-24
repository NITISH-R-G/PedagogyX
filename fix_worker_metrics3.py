import sys

filepath = 'services/worker-metrics/tests/test_metrics_main.py'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('from worker.main import', 'from worker.main import  # type: ignore')

with open(filepath, 'w') as f:
    f.write(content)
