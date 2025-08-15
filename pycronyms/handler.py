from typing import Optional, TypeVar, Generic, NoReturn
from abc import ABC, abstractmethod
from pathlib import Path

T = TypeVar("T")


class Handler(ABC, Generic[T]):
    """This is an interface for an hanlder. It should be able to
    take a filepath as parameter and to read and/or write to it."""

    name: str

    def __init__(self, filepath: Path, data: Optional[T] = None):
        self.filepath = filepath
        self.data = data

    @abstractmethod
    def read(self) -> T:
        """This method should read the filepath data and returns it in an arbitrary format.

        Returns:
            T: The data.
        """

    @abstractmethod
    def write(self, data: Optional[T] = None) -> NoReturn:
        """This method should write data to the file passed via the constructor method.
        It should write self.data or data if its non-none.

        Args:
            data (Optional[T]): An optional parameter to override the written data.
        """
