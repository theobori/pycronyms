from typing import Set
from abc import abstractmethod
from functools import cache

from pycronyms._common import create_recursive_dict
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.acronym import Acronym
from pycronyms.exceptions import MissingAcronymError, FetchAcronymsError
from pycronyms.provider import Provider
from pycronyms.acronyms import Acronyms, AcronymsDict, dict_from_acronyms


class ProviderHelper(Provider):
    """This is a helper class that provide features to easily manage acronyms fetch and read.

    The internal data structure has been thought to represents the datas
    in an intuitive and friendly way and to have an efficient time complexity."""

    def __init__(self):
        self._acronyms: Acronyms = create_recursive_dict(Acronym, depth=3)
        self._amount = 0

    def __repr__(self) -> str:
        return f"Acronyms provider '{self.name}'"

    @property
    def amount(self) -> int:
        return self._amount

    @property
    def acronyms(self) -> Acronyms:
        return self._acronyms

    @property
    def acronyms_dict(self) -> AcronymsDict:
        """Returns a dictionnary where each container is a Python built-in dictionnary.

        Returns:
            AcronymsDict: The dictionnary new object.
        """

        return dict_from_acronyms(self._acronyms)

    @abstractmethod
    def _fetch_acronyms(self, language: Language, category: Category) -> Set[Acronym]:
        """This mehod fetch the data, then `fetch_acronyms` is going
        to automatically manage the datas.

        Having this method avoid us to have a decorator to put on every different providers
        and offer the `abc` module mechanisms.

        Args:
            language (Language): The language.
            category (Category): The category.

        Returns:
            Set[Acronym]: The set of acronyms found."""

    def __fetch_acronyms_wrapper(
        self, language: Language, category: Category
    ) -> Set[Acronym]:
        """Fetch the acronyms then compute metrics with it.

        Args:
            language (Language): The language.
            category (Category): The category.

        Returns:
            Set[Acronym]: The set of acronyms found.
        """

        acronyms = self._fetch_acronyms(language, category)

        self._amount += len(acronyms)

        return acronyms

    @cache
    def fetch_acronyms(self, language: Language, category: Category) -> Set[Acronym]:
        """_summary_

        Args:
            language (Language): The language corresponds to the language of the words in each letter of the acronym.
            category (Category): The category.

        Raises:
            FetchAcronymsError: An error occured during acronyms fetching.

        Returns:
            Set[Acronym]: The set of acronyms found.
        """

        acronyms: Set[Acronym]

        try:
            acronyms = self.__fetch_acronyms_wrapper(language, category)
        except Exception as e:
            raise FetchAcronymsError(language=language, category=category) from e

        d = self._acronyms[language][category]

        for acronym in acronyms:
            if acronym.name in d:
                d[acronym.name].add_extra(acronym)
            else:
                d[acronym.name] = acronym

        return acronyms

    def get_acronym(self, name: str, language: Language, category: Category) -> Acronym:
        """Retrieve a fetched acronym.

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
