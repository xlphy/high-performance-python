"""decorator to time any function"""
import time
from functools import wraps


def timefn(fn):
    @wraps(fn)
    def measure_time(*args, **kwargs):
        start = time.time()
        res = fn(*args, **kwargs)
        end = time.time()
        print(f"@timefn: {fn.__name__} took {end - start} seconds")
        return res
    return measure_time
