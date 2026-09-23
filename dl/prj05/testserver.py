import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import threading

URL = "http://192.168.40.3:8001/book"

# 강도를 조절하는 부분
TOTAL_REQUESTS = 2_00
CONCURRENCY = 300

success = 0
failed = 0
elapsed_times = []

# 스레드마다 Session 하나씩 사용
local = threading.local()

def get_session():
    if not hasattr(local, "session"):
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=1000,
            max_retries=0
        )
        session.mount("http://", adapter)
        local.session = session

    return local.session


def request():
    start = time.perf_counter()

    try:
        session = get_session()
        r = session.get(URL, timeout=5)

        elapsed = time.perf_counter() - start
        return r.status_code, elapsed

    except Exception:
        return None, time.perf_counter() - start


start = time.perf_counter()

with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
    futures = [
        executor.submit(request)
        for _ in range(TOTAL_REQUESTS)
    ]

    for future in as_completed(futures):
        status, elapsed = future.result()

        if status == 200:
            success += 1
        else:
            failed += 1

        elapsed_times.append(elapsed)

total_time = time.perf_counter() - start

print("\n===== 결과 =====")
print(f"총 요청: {TOTAL_REQUESTS:,}")
print(f"성공: {success:,}")
print(f"실패: {failed:,}")
print(f"총 시간: {total_time:.2f}초")
print(f"RPS: {TOTAL_REQUESTS / total_time:.2f}")
print(f"평균 응답시간: {sum(elapsed_times) / len(elapsed_times) * 1000:.2f} ms")
print(f"최대 응답시간: {max(elapsed_times) * 1000:.2f} ms")