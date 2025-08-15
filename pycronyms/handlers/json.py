from typing import Any, Optional, NoReturn
from pathlib import Path

from pycronyms.handler_acronyms import HandlerAcronyms
from pycronyms.acronyms import (
    Acronyms,
    AcronymsDict,
    dict_from_acronyms,
    acronyms_from_dict,
)
from pycronyms.exceptions import HandlerError

import orjson


def read_json_file(path: Path) -> Any:
    """Convert the Python object to a Python bytes object, then writting
        it to the given file.

    Args:
        obj (Any): The Python object.
        path (Path): The file path.
    """

    obj: Any

    with open(path, "rb") as f:
        obj = orjson.loads(f.read())

    return obj


def write_to_json(obj: Any, path: Path) -> NoReturn:
    """Convert the Python object to a Python bytes object, then writting
        it to the given file.

    Args:
        obj (Any): The Python object.
        path (Path): The file path.
    """

    with open(path, "w+") as f:
        obj_bytes = orjson.dumps(obj, option=orjson.OPT_INDENT_2)
        f.write(obj_bytes.decode())


class HandlerJSON(HandlerAcronyms):
    """JSON acronyms handler. It reads and writes JSON files."""

    name = "json"

    def read(self) -> Acronyms:
        """Read a JSON file then get a Acronyms Python object with its content.

        Raises:
            HandlerError: An error occured when reading the JSON filepath.

        Returns:
            Acronyms: The acronyms.
        """

        acronyms_dict: AcronymsDict
        try:
            acronyms_dict = read_json_file(self.filepath)
        except Exception as e:
            raise HandlerError(self.name, self.filepath) from e

        acronyms = acronyms_from_dict(acronyms_dict)
        self.data = acronyms

        return self.data

    def write(self, data: Optional[Acronyms] = None) -> NoReturn:
        """Write to a JSON file from a Acronyms Python object.

        Args:
            data (Optional[Acronyms], optional): Optional acronyms to override the content to write to the file. Defaults to None.

        Raises:
            HandlerError: An error occured when writting to the JSON file.
        """

        arg: Acronyms
        if data:
            arg = data
        else:
            arg = self.data

        d = dict_from_acronyms(arg)

        try:
            write_to_json(d, self.filepath)
        except Exception as e:
            raise HandlerError(self.name, self.filepath) from e
