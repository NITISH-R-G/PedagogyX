import sys

filepath = 'services/worker-metrics/worker/metrics_main.py'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('import redis', 'import redis  # type: ignore')

with open(filepath, 'w') as f:
    f.write(content)

filepath = 'services/api/app/queue.py'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('import redis', 'import redis  # type: ignore')

with open(filepath, 'w') as f:
    f.write(content)

filepath = 'services/worker-asr/worker/asr_main.py'
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace('import redis', 'import redis  # type: ignore')
content = content.replace('from worker.processor', 'from worker.processor  # type: ignore')

with open(filepath, 'w') as f:
    f.write(content)
