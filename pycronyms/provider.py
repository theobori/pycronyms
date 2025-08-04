from typing import Set, Any
from abc import ABC, abstractmethod

from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.acronym import Acronym


class Provider(ABC):
    """This is the interface for an acronyms provider."""

    name: str

    @abstractmethod
    def fetch_acronyms(self, language: Language, category: Category) -> Set[Acronym]:
        """It should returns a set of acronyms object corresponding to a given language and category.

        Args:
            language (Language): The language corresponds to the language of the words in each letter of the acronym.
            category (Category): The category.

        Returns:
            Set[Acronym]: The set of acronyms found.
        """

    @abstractmethod
    def get_acronym(self, name: str, language: Language, category: Category) -> Acronym:
        """It should returns the associated acronym object.

        Args:
            name (str): The acronym name.
            language (Language): The language.
            category (Category): The category.

        Returns:
            Acronym: The correspoding acronym object.
        """

    @property
    @abstractmethod
    def acronyms(self) -> Any:
        """Should returns every fetched acronyms since the beginning."""
