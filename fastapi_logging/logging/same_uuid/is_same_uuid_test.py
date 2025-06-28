from concurrent.futures import ThreadPoolExecutor
import requests


def post(test_id: str):
    res = requests.get(f"http://localhost:9999/{test_id}")
    return res.json()


with ThreadPoolExecutor(max_workers=10) as executor:
    for i in range(10):
        executor.submit(post, i)
