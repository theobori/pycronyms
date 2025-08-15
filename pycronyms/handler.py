from typing import Optional, TypeVar, Generic, NoReturn
from abc import ABC, abstractmethod
from pathlib import Path

T = TypeVar("T")


class Handler(ABC, Generic[T]):
    """This is an interface for an hanlder. It should be able to
    take a filepath as parameter and to read and/or write to it."""

    name: str

    @classmethod
    @abstractmethod
    def read(cls, filepath: Path) -> T:
        """This method should read the filepath data and returns it in an arbitrary format.

        Args:
            filepath (Path): The destination JSON file path.

        Returns:
            T: The data.
        """

    @classmethod
    @abstractmethod
    def write(cls, filepath: Path, data: T) -> NoReturn:
        """This method should write data to the file passed via the constructor method.
        It should write self.data or data if its non-none.

        Args:
            filepath (Path): The destination JSON file path.
            data (T): An optional parameter to override the written data.
        """
