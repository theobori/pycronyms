import re

from typing import Set
from functools import cache

from pycronyms.provider_helper import ProviderHelper
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.acronym import Acronym
from pycronyms.exceptions import FetchAcronymsError
from pycronyms._common import remove_html_content

import wikipedia

from pydantic import ValidationError

COMPUTER_SCIENCE_RE: re.Pattern = re.compile(r"<li><a href=.*>(.*)<\/a>—(.*)<\/li>")
IT_RE: re.Pattern = re.compile(r"""<td><a href=.*>(.*)<\/a>
<\/td>
<td>(.*)
<\/td>""")


class Wikipedia(ProviderHelper):
    """The Wikipedia provider. This provider mainly make requests to the official Wikipedia API.

    Disclaimer, if you want to use this provider, its better to not use a mobile network,
    because it could use an IPv6 address and then you could be blocked.

    For more details, see https://en.wikipedia.org/wiki/Wikipedia:Advice_to_T-Mobile_IPv6_users.
    """

    name = "wikipedia"

    def __init__(self):
        super().__init__()

    @cache
    def __fetch_html(self, title: str) -> str:
        """Fetch a Wikipedia HTML page.

        Args:
            title (str): The Wikipedia page title.

        Raises:
            FetchAcronymsError: An error occured when requesting the Wikipedia API.

        Returns:
            str: The HTML content.
        """

        html: str

        try:
            page = wikipedia.page(title=title)
            html = page.html()
        except Exception as e:
            raise FetchAcronymsError(
                f"Unable to get the wikipedia page with title {title}"
            ) from e

        return html

    def __fetch_acronyms(self, title: str, regex: re.Pattern) -> Set[Acronym]:
        """Fetch Wikipedia acronyms helper function.

        Args:
            title (str): The Wikipedia page title.
            regex (re.Pattern): The regex that must match an acronym and its meaning.

        Raises:
            FetchAcronymsError: An error occured when requesting the Wikipedia API.

        Returns:
            Set[Acronym]: The fetched acronyms.
        """

        try:
            html = self.__fetch_html(title)
        except FetchAcronymsError as e:
            raise e

        matches = regex.findall(html)

        acronyms: Set[Acronym] = set()
        for name, meaning in matches:
            meaning = remove_html_content(meaning)

            acronym: Acronym
            try:
                acronym = Acronym(name=name, meaning=meaning, provider=self.name)
            except ValidationError as e:
                continue

            acronyms.add(acronym)

        return acronyms

    @cache
    def _fetch_acronyms_information_technology(self) -> Set[Acronym]:
        """_summary_

        Returns:
            Set[Acronym]: The fetched acronyms.
        """

        return self.__fetch_acronyms(
            "List_of_information_technology_initialisms", IT_RE
        )

    @cache
    def _fetch_acronyms_computer_science(self) -> Set[Acronym]:
        """Fetch the Wikipedia acronyms about computer science.

        Raises:
            FetchAcronymsError: An error occured when requesting the Wikipedia API.

        Returns:
            Set[Acronym]: The fetched acronyms.
        """

        return self.__fetch_acronyms(
            "List_of_computing_and_IT_abbreviations", COMPUTER_SCIENCE_RE
        )

    @cache
    def _fetch_acronyms(self, language: Language, category: Category) -> Set[Acronym]:
        """Fetch the Wikipedia acronyms with a specific language and category.

        Args:
            language (Language): The language.
            category (Category): The category.

        Raises:
            FetchAcronymsError: An error occured when requesting the Wikipedia API.

        Returns:
            Set[Acronym]: The fetched acronyms.
        """

        acronyms = set()

        # Wikipedia seems to not have other language acronyms
        if language != Language.ENGLISH:
            return acronyms

        match category:
            case Category.COMPUTER_SCIENCE:
                acronyms = acronyms.union(self._fetch_acronyms_computer_science())
                acronyms = acronyms.union(self._fetch_acronyms_information_technology())
            case Category.COMMON:
                pass

        for a in acronyms:
            print(a)

        return acronyms
