""" Модуль декораторов для логирования работы функций """

from functools import wraps
import logging
import inspect


def log(logger=logging):
    """
    Функция-декоратор для логирования работы функций
    """

    def log_wrap(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logger.info('function "%s" was called from function "%s" with arguments %s and named arguments %s '
                        'result is %s',
                        func.__name__, inspect.stack()[1].function, args, kwargs, result)
            return result

        return wrapper

    return log_wrap


class Log:
    """
    Класс для логирования работы функций
    """

    def __init__(self, logger=logging):
        self.logger = logger

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self.logger.info(
                'function %s was called from function %s with arguments %s and named arguments %s result is %s',
                func.__name__, inspect.stack()[1].function, args, kwargs, result)
            return result

        return wrapper
