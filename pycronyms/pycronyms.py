import logging

from time import time
from typing import Set, Self, Dict, List
from collections import OrderedDict

from pycronyms.provider_helper import ProviderHelper, Provider
from pycronyms.acronym import Acronym
from pycronyms.exceptions import FetchAcronymsError
from pycronyms.language import Language
from pycronyms.category import Category

logger = logging.getLogger("pycronyms.aggregator")
logger.disabled = True  # Should be read-only


class Pycronyms(ProviderHelper):
    """This is a special provider. It depends of Provider object instances passed to this class.

    The aim of this provider is to aggregate every acronyms from the given providers.
    """

    name = "aggregator"

    def __init__(self):
        super().__init__()

        self.__providers: OrderedDict[str, Provider] = OrderedDict()

    def add_provider(self, provider: Provider) -> Self:
        """Add a provider that will fetch acronyms

        Args:
            provider (Provider): A provider instance.

        Returns:
            Self: The object instance itself.
        """

        self.__providers[provider.name] = provider

        return self

    def _fetch_acronyms(self, language: Language, category: Category) -> Set[Acronym]:
        acronyms = set()

        for provider in self.__providers.values():
            try:
                fetched_acronyms = provider.fetch_acronyms(language, category)
                amount = len(fetched_acronyms)

                if amount > 0:
                    logger.info(
                        f"The provider '{provider.name}' fetched {amount} acronyms "
                        f"for the language '{language.iso_639_1_code}' "
                        f"and the category '{category.fancy_value()}'"
                    )

                acronyms = acronyms.union(fetched_acronyms)
            except FetchAcronymsError as e:
                continue

        return acronyms

    def fetch_all(self) -> Set[Acronym]:
        """It will fetch every acronyms for every possible pair of language and category.

        Returns:
            Set[Acronym]: The fetched acronyms.
        """

        acronyms = set()

        logger.info("Started to fetch all acronyms")

        start = time()

        for language in Language:
            for category in Category:
                acronyms = acronyms.union(self.fetch_acronyms(language, category))

        end = time() - start

        logger.info(f"Finished to fetch all acronyms in {end:.2f} seconds")

        return acronyms

    @property
    def provider_names(self) -> List[str]:
        return self.__providers.keys()
