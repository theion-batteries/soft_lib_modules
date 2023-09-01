from abc import ABC, abstractmethod


class Client(ABC):
    """Abstract base class for all Client communication"""

    @abstractmethod
    def __init__(self, ip: str, port: int, buffer_size: int):
        pass

    @abstractmethod
    async def connect(self) -> bool | Exception:
        """establish connection to the client

        Returns
        --------
        bool | Exception

        """
        pass

    @abstractmethod
    async def send_message(self, data: str) -> bool | Exception:
        """send message to the client

        Parameters
        -------------
        data: str

        Returns
        --------
        bool | Exception

        """

        pass

    @abstractmethod
    async def read_message_until(self, delimiter: str = "\n") -> str | Exception:
        """read message until delimiter is found

        Parameters
        ----------
        delimeter : str


        Returns
        --------
        str | Exception

        """

        pass

    @abstractmethod
    async def read_message(self) -> str:
        pass

    @abstractmethod
    async def read_message_line(self) -> str:
        pass

    @abstractmethod
    async def close(self):
        """close the connection"""

        pass
