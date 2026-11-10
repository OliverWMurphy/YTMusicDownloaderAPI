import functools


def log_name(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("Calling %s", func.__name__)
        return func(*args, **kwargs)
    return wrapper
