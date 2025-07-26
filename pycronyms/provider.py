from typing import Dict, List, Any
from abc import ABC, abstractmethod

from pycronyms._common import create_recursive_dict
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.acronym import Acronym
from pycronyms.exceptions import MissingAcronymError, FetchAcronymsError


class Provider(ABC):
    """This is the interface for an acronyms provider."""

    name: str

    @abstractmethod
    def fetch_acronyms(self, language: Language, category: Category) -> List[Acronym]:
        """It should returns a list of acronyms object corresponding to a given language and category.

        Args:
            language (Language): The language corresponds to the language of the words in each letter of the acronym.
            category (Category): The category.

        Returns:
            List[Acronym]: The list of acronyms found.
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


class ProviderHelper(Provider):
    """This is a helper class that provide features to easily manage acronyms fetch and read.

    The internal data structure has been thought to represents the datas
    in an intuitive and friendly way and to have an efficient time complexity."""

    def __init__(self):
        self._acronyms: Dict[Language, Dict[Category, Dict[str, Acronym]]] = (
            create_recursive_dict(str, depth=3)
        )
        self._amount = 0

    def __repr__(self) -> str:
        return f"Acronyms provider '{self.name}'"

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def acronyms(self) -> dict:
        return self._acronyms

    @abstractmethod
    def _fetch_acronyms(self, language: Language, category: Category) -> List[Acronym]:
        """This mehod fetch the data, then `fetch_acronyms` is going
        to automatically manage the datas.

        Having this method avoid us to have a decorator to put on every different providers
        and offer the `abc` module mechanisms.

        Args:
            language (Language): The language.
            category (Category): The category.

        Returns:
            List[Acronym]: The list of acronyms found."""

    def __fetch_acronyms_wrapper(
        self, language: Language, category: Category
    ) -> List[Acronym]:
        """Fetch the acronyms then compute metrics with it.

        Args:
            language (Language): The language.
            category (Category): The category.

        Returns:
            List[Acronym]: The list of acronyms found.
        """

        acronyms = self._fetch_acronyms(language, category)

        self._amount += len(acronyms)

        return acronyms

    def fetch_acronyms(self, language: Language, category: Category) -> List[Acronym]:
        """_summary_

        Args:
            language (Language): The language corresponds to the language of the words in each letter of the acronym.
            category (Category): The category.

        Raises:
            FetchAcronymsError: An error occured during acronyms fetching.

        Returns:
            List[Acronym]: The list of acronyms found.
        """

        acronyms: List[Acronym]

        try:
            acronyms = self.__fetch_acronyms_wrapper(language, category)
        except Exception as e:
            raise FetchAcronymsError(language, category) from e

        d = self._acronyms[language][category]

        for acronym in acronyms:
            if acronym.name in d:
                d[acronym.name].extras.add(acronym)
            else:
                d[acronym.name] = acronym

        return acronyms

    def get_acronym(self, name: str, language: Language, category: Category) -> Acronym:
        """_summary_

        Args:
            name (str): The acronym name.
            language (Language): The language.
            category (Category): The category.

        Raises:
            MissingAcronymError: The requested acronym has no been fetched.

        Returns:
            Acronym: The correspoding acronym object.
        """

        d = self._acronyms[language][category]

        if not name in d:
            raise MissingAcronymError(name, language, category)

        return d[name]
