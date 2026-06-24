def fix(filepath, replacement):
    with open(filepath, 'r') as f:
        content = f.read()
    content = content.replace('worker.main', replacement)
    with open(filepath, 'w') as f:
        f.write(content)

fix('services/worker-metrics/Dockerfile', 'worker.metrics_main')
fix('services/worker-asr/Dockerfile', 'worker.asr_main')
