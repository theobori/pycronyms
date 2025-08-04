from typing import Set, Dict, List
from functools import cache

from pycronyms.provider_helper import ProviderHelper
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.acronym import Acronym

from pydantic import ValidationError

CUSTOM_ACRONYMS: Dict[Language, Dict[Category, dict]] = {
    Language.FRENCH: {
        Category.COMMON: {
            "COM": {"meaning": "Collectivité d’outre-mer"},
            "TGV": {
                "meaning": "Train à Grande Vitesse",
                "extras": ["Très Grande Vitesse"],
            },
        },
        Category.COMPUTER_SCIENCE: {
            "UC": {"meaning": "Unité Centrale"},
            "DD": {"meaning": "Disque dur"},
        },
    }
}


class Custom(ProviderHelper):
    """A custom provider returning arbitrary acronyms."""

    name = "custom"

    def __init__(self):
        super().__init__()

    @cache
    def _fetch_acronyms(self, language: Language, category: Category) -> Set[Acronym]:
        """Returns acronyms with a specific language and category.

        Args:
            language (Language): The language.
            category (Category): The category.

        Returns:
            Set[Acronym]: The fetched acronyms.
        """

        acronyms = set()

        if not language in CUSTOM_ACRONYMS:
            return acronyms

        if not category in CUSTOM_ACRONYMS[language]:
            return acronyms

        acronyms_dict = CUSTOM_ACRONYMS[language][category]

        for name, raw in acronyms_dict.items():
            acronym: Acronym

            try:
                acronym = Acronym(name=name, meaning=raw["meaning"], provider=self.name)
            except ValidationError as e:
                continue

            acronyms.add(acronym)

            extras: List[str] = []
            if "extras" in raw:
                extras = raw["extras"]

            for extra in extras:
                try:
                    acronyms.add(
                        Acronym(name=name, meaning=extra, provider=acronym.provider)
                    )
                except ValidationError as e:
                    continue

        return acronyms
