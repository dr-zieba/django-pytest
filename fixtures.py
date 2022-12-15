from datetime import datetime

import pytest


@pytest.fixture
def time_tracker():
    start = datetime.now()
    yield
    end = datetime.now()
    time = end - start
    print(f'\nRun time: {time}')