from typing import Optional

from pycronyms.language import Language
from pycronyms.category import Category


class PycronymsError(Exception):
    """Pycronyms base error."""


class FetchAcronymsError(PycronymsError):
    """Unable to fetch acronyms error.
    Should be used for the providers."""

    def __init__(
        self,
        message: Optional[str] = None,
        language: Optional[Language] = None,
        category: Optional[Category] = None,
    ):
        super().__init__()

        self.message = message
        self.language = language
        self.category = category

    def __str__(self):
        if self.language is None or self.category is None:
            return self.message or "An error occured during acronyms fetching"

        return (
            "Unable to fetch acronyms "
            f"with language {self.language.value} and "
            f"category {self.category.fancy()}"
        )


class MissingAcronymError(PycronymsError):
    """Missing an acronym error."""

    def __init__(self, name: str, language: Language, category: Category):
        super().__init__()

        self.name = name
        self.language = language
        self.category = category

    def __str__(self):
        return (
            f"The acronym '{self.name}' "
            f"with language {self.language.value} and "
            f"category {self.category.fancy()} is missing"
        )
