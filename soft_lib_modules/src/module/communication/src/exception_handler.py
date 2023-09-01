import functools
import logging

from .response import Mode, Response


def StreamReadExceptionHandler(func):
    @functools.wraps(func)
    async def stream_function(*args, **kwargs):
        response: Response = None
        try:
            data = await func(*args, **kwargs)
            data = data.replace(b"\r\n", b"").decode()
            check_unicode: bool = lambda data: data.isascii()
            if not check_unicode(data):
                raise UnicodeError
            response = Response(True, "", Mode.READ, data)
        except Exception as e:
            response = Response(False, "", Mode.READ, e)
        return response

    return stream_function


def StreamExceptionHandler(func):
    @functools.wraps(func)
    async def stream_function(*args, **kwargs):
        response: Response = None
        command: str = ""
        mode: Mode = None
        if len(args) == 2:
            command = args[1].rstrip("\r\n")
            mode = Mode.SEND
        else:
            mode = Mode.CONNECTION
        try:
            await func(*args, **kwargs)
            message = "success"
            response = Response(True, command, mode, message)
        except Exception as e:
            response = Response(False, command, mode, e)
        return response

    return stream_function


class StreamConnectionLostException(Exception):
    def __init__(self, message):
        pass


class TCPClientException(Exception):
    def __init__(self, message):
        pass
