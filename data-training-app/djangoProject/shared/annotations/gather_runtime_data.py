import functools
import time


def save_model_to_db(target):
    @functools.wraps(target)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = target(*args, **kwargs)
        result.runtime = time.perf_counter() - start
        return result

    return _wrapper
