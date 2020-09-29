'''
    PoliteInfiniteComputer created by acwoss - https://repl.it/@acwoss/PoliteInfiniteComputer
'''

from multiprocessing import TimeoutError
from multiprocessing.pool import ThreadPool

def timeout(seconds):
    def decorator(function):
        def wrapper(*args, **kwargs):
            pool = ThreadPool(processes=1)
            result = pool.apply_async(function, args=args, kwds=kwargs)
            try:
                return result.get(timeout=seconds)
            except TimeoutError as e:
                return e
        return wrapper
    return decorator


# alterado a partir daqui

@timeout(60)
def keyboard_reading(text):
    print(text, end="")
    return input()

def get_answer(msg=""):
    result = keyboard_reading(msg)

    if isinstance(result, TimeoutError):
        return False
    else:
        return result


