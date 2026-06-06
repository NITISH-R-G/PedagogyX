import time
import os
import tempfile
import boto3
from botocore.stub import Stubber
from concurrent.futures import ThreadPoolExecutor, as_completed

def _s3():
    return boto3.client(
        "s3",
        region_name="us-east-1",
    )

def download_sequential(client, chunks):
    tmp = tempfile.NamedTemporaryFile(suffix=".bin", delete=False)
    path = tmp.name
    tmp.close()

    start = time.perf_counter()
    with open(path, "wb") as out:
        for _idx, key in chunks:
            obj = client.get_object(Bucket="test-bucket", Key=key)
            out.write(obj["Body"].read())
    elapsed = time.perf_counter() - start
    os.unlink(path)
    return elapsed

def _download_chunk(client, key):
    obj = client.get_object(Bucket="test-bucket", Key=key)
    return obj["Body"].read()

def download_concurrent(client, chunks):
    tmp = tempfile.NamedTemporaryFile(suffix=".bin", delete=False)
    path = tmp.name
    tmp.close()

    start = time.perf_counter()

    results = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_idx = {executor.submit(_download_chunk, client, key): idx for idx, key in chunks}
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as exc:
                raise RuntimeError(f"minio get concurrent: {exc}") from exc

    with open(path, "wb") as out:
        # write in order
        for idx in sorted(results.keys()):
            out.write(results[idx])

    elapsed = time.perf_counter() - start
    os.unlink(path)
    return elapsed

if __name__ == "__main__":
    import io
    from botocore.response import StreamingBody

    client = _s3()
    stubber = Stubber(client)

    # Let's mock a delay in reading the body to simulate network IO
    class DelayedStreamingBody(StreamingBody):
        def read(self, amt=None):
            time.sleep(0.05) # 50ms delay per chunk to simulate network
            return super().read(amt)

    chunks = [(i, f"bench-chunk-{i}") for i in range(20)]

    for i in range(20):
        # We need to stub each get_object call for sequential
        response = {
            'Body': DelayedStreamingBody(io.BytesIO(b"0" * 1024), 1024)
        }
        expected_params = {'Bucket': 'test-bucket', 'Key': f'bench-chunk-{i}'}
        stubber.add_response('get_object', response, expected_params)

    stubber.activate()

    print("Running sequential...")
    seq_time = download_sequential(client, chunks)
    print(f"Sequential: {seq_time:.4f}s")

    stubber.deactivate()

    stubber = Stubber(client)

    # We must add responses in the order they will be called.
    # Concurrent might call them in any order! Stubber requires strict order unless we use ANY for params
    # Or we can just use ANY params.
    from botocore.stub import ANY
    for i in range(20):
        response = {
            'Body': DelayedStreamingBody(io.BytesIO(b"0" * 1024), 1024)
        }
        expected_params = {'Bucket': 'test-bucket', 'Key': ANY}
        stubber.add_response('get_object', response, expected_params)

    stubber.activate()
    print("Running concurrent...")
    con_time = download_concurrent(client, chunks)
    print(f"Concurrent: {con_time:.4f}s")

    if seq_time > 0:
        improvement = (seq_time - con_time) / seq_time * 100
        print(f"Improvement: {improvement:.2f}%")
