from typing import Optional
from pathlib import Path

from pycronyms.handler import Handler
from pycronyms.provider_helper import Acronyms
from pycronyms.acronym import Acronym
from pycronyms._common import create_recursive_dict


class HandlerAcronyms(Handler[Acronyms]):
    """Handler `Acronyms` oriented."""

    def __init__(self, filepath: Path, data: Optional[Acronyms] = None):
        super().__init__(filepath, data)

        if data:
            self.data = data
        else:
            self.data: Acronyms = create_recursive_dict(Acronym, 3)
