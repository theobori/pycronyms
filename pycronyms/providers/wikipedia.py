from typing import List
from functools import cache

from pycronyms.provider import ProviderHelper
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.acronym import Acronym
from pycronyms.exceptions import MissingAcronymError, FetchAcronymsError

import wikipedia


class Wikipedia(ProviderHelper):
    """The Wikipedia provider. This provider mainly make requests to the official Wikipedia API.

    Disclaimer, if you want to use this provider, its better to not use a mobile network,
    because it could use an IPv6 address and then you could be blocked.

    For more details, see https://en.wikipedia.org/wiki/Wikipedia:Advice_to_T-Mobile_IPv6_users.
    """

    name = "wikipedia"

    def __init__(self):
        super().__init__()

    def __fetch_acronyms_information_technology(self, acronyms: List[Acronym]):
        return []

    @cache
    def _fetch_acronyms_computer_science(self) -> List[Acronym]:
        return []

    @cache
    def _fetch_acronyms(self, language: Language, category: Category) -> List[Acronym]:
        acronyms = set()

        # Wikipedia seems to not have other language acronyms
        if language != Language.ENGLISH:
            return acronyms

        match category:
            case Category.COMPUTER_SCIENCE:
                acronyms = self._fetch_acronyms_computer_science()

        return acronyms
