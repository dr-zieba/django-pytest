from datetime import datetime, timedelta
from typing import Callable
import pytest


@pytest.fixture
def time_tracker():
    start = datetime.now()
    yield
    end = datetime.now()
    time = end - start
    print(f"\nRun time: {time}")


class PerformanceException(Exception):
    def __init__(self, runtime: timedelta, runtime_limit: timedelta):
        self.runtime = runtime
        self.limit = runtime_limit

    def __str__(self):
        return (
            f"Performance test failed, runtime={self.runtime}, time limit: {self.limit}"
        )


def track_performace(method: Callable, runtime_limit=timedelta(seconds=2)):
    def run_function_and_validate_runtime(*args, **kw):
        start = datetime.now()
        result = method(*args, **kw)
        end = datetime.now()
        runtime = end - start
        print(f"\nRun time: {runtime}")

        if runtime > runtime_limit:
            raise PerformanceException(runtime=runtime, runtime_limit=runtime_limit)

        return result

    return run_function_and_validate_runtime
