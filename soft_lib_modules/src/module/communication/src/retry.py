import logging
from functools import wraps

from .response import Response


def handle_response(response: list[Response] | Response) -> bool:
    result = True
    if isinstance(response, list):
        for r in response:
            result = r.result and result

    else:
        result = response.result
    return result


def retry(times, exceptions):
    """
    Retry Decorator
    Retries the wrapped function/method `times` times if the exceptions listed
    in ``exceptions`` are thrown
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """

    def decorator(func):
        @wraps(func)
        async def newfn(*args, **kwargs):
            attempt = 0
            result = None
            while attempt < times:
                result = await func(*args, **kwargs)

                if not handle_response(result):
                    logging.critical(
                        "Exception thrown on run {}(), attempt  {} of {} due to {}".format(
                            func.__name__, attempt + 1, times, result
                        )
                    )
                    attempt += 1
                    continue

                else:
                    break

            return result

        return newfn

    return decorator
