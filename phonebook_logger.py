import logging
import time


logger = logging.getLogger("LOG")
logger.setLevel(logging.INFO)
logging.basicConfig(filename="proglog.log", level=logging.INFO)


def log_decorator(logger):
    def decorator(func):
        def wrapper(*args, **kwargs):
            name = func.__name__
            try:
                t = time.time()
                logger.info('Функция:{} Аргументы:{},{} Время выполнения:{}'.format(name, args, kwargs, (time.time() - t)))
                return func(*args, **kwargs)
            except Exception as ex:
                err = name
                logger.exception(err)
                print('Ошибка {} в методе {}'.format(type(ex).__name__, err))
        return wrapper
    return decorator
