from pycronyms.language import Language
from pycronyms.category import Category


class PycronymsError(Exception):
    """Pycronyms base error."""


class FetchAcronymsError(PycronymsError):
    """Unable to fetch acronyms error.
    Should be used for the providers."""

    def __init__(self, language: Language, category: Category):
        super().__init__()

        self.language = language
        self.category = category

    def __str__(self):
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
