from typing import Dict

from pycronyms._common import create_recursive_dict
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.acronym import Acronym

type Acronyms = Dict[Language, Dict[Category, Dict[str, Acronym]]]

type AcronymsDict = Dict[str, Dict[str, Dict[str, dict]]]


def dict_from_acronyms(acronyms: Acronyms) -> AcronymsDict:
    """Returns a dictionnary where each container is a Python built-in dictionnary.

    Args:
        acronyms (Acronyms): The acronyms.

    Returns:
        AcronymsDict: The dictionnary new object.
    """

    d: AcronymsDict = create_recursive_dict(Acronym, depth=3)

    for language, lv in acronyms.items():
        for category, cv in lv.items():
            for acronym_name, acronym in cv.items():
                acronym_dict = acronym.to_dict()
                del acronym_dict["name"]

                d[language.iso_639_1_code][category.value][acronym_name] = acronym_dict

    return d


def acronyms_from_dict(acronyms_dict: AcronymsDict) -> Acronyms:
    """Build a dict of acronyms with language and category.

    Args:
        acronyms_dict (AcronymsDict): The acronyms Python dictionnary.

    Returns:
        Acronyms: The acronyms.
    """

    acronyms: Acronyms = create_recursive_dict(Acronym, depth=3)

    for lk, lv in acronyms_dict.items():
        for ck, cv in lv.items():
            for acronym_name, d in cv.items():
                # It allows us to not overwrite the acronyms_dict passed to the function
                d_copy = d | {"name": acronym_name}

                acronym = Acronym.from_dict(d_copy)

                l = Language._value2member_map_[lk]
                c = Category._value2member_map_[ck]

                acronyms[l][c][acronym_name] = acronym

        return acronyms
