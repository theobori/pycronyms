import os
import orjson
import logging
import sys
import random

from typing import NoReturn, Any, Optional, List, Dict, Tuple, Set
from argparse import ArgumentParser, RawTextHelpFormatter
from pathlib import Path
from enum import Enum

from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.exceptions import PycronymsError
from pycronyms.provider_helper import AcronymsDict

from pycronyms.cli.pycronyms_generate import OUTPUT_DIRNAME

from thefuzz import process


logger = logging.getLogger(__file__)

BASE_DIRPATH = Path(os.path.dirname(__file__))
EMBEDDED_ACRONYMS_DIR = BASE_DIRPATH / ".." / OUTPUT_DIRNAME


def _enum_description_list(
    name: str, e: Optional[Enum] = None, values: Optional[List[str]] = None
) -> str:
    """This is an helper function used to list CLI choices represented
    as an enum into Python string.

    It returns a formatted string representing this list.

    Args:
        name (str): The list name.
        e (Optional[Enum], optional): The optional enum. Defaults to None.
        values (Optional[List[str]], optional): Optional values that override the enum. Defaults to None.

    Returns:
        str: The new formatted string.
    """

    values: List[str]

    name = name.upper()

    if not e is None:
        values = e._member_map_.values()
    else:
        values = values or []

    if len(values) == 0:
        return f"No values are available for {name}."

    values_str = [f"'{value}'\n" for value in values]
    values_str = "- " + "- ".join(values_str)

    description = f"""
The following values for {name} are available.
{values_str}"""

    return description


def create_parser() -> ArgumentParser:
    """Creating a parser.

    Returns:
        ArgumentParser: The created parser.
    """

    language_description = _enum_description_list(
        "language", values=[l.iso_639_1_code for l in Language]
    )
    category_description = _enum_description_list("category", e=Category)

    description = f"""
Guess acronym meanings.

{language_description}
{category_description}
"""

    parser = ArgumentParser(
        description=description, formatter_class=RawTextHelpFormatter
    )

    parser.add_argument("-l", "--language", required=False, default=None, type=str)
    parser.add_argument("-c", "--category", required=False, default=None, type=str)
    parser.add_argument("-n", "--name", required=False, default=None, type=str)

    return parser


def read_json_file(path: Path) -> Any:
    """Convert the Python object to a Python bytes object, then writting
        it to the given file.

    Args:
        obj (Any): The Python object.
        path (Path): The file path.
    """

    obj: Any

    with open(path, "rb") as f:
        obj = orjson.loads(f.read())

    return obj


def get_meanings(acronym_dict: dict) -> Set[str]:
    """Return a set containing every meaning of a given acronym.

    Args:
        acronym_dict (dict): Every acronym dict.

    Returns:
        Set[str]: The acronym meanings.
    """

    meanings: Set[str] = {acronym_dict["meaning"]}

    if "extras" in acronym_dict:
        extras = [extra["meaning"] for extra in acronym_dict["extras"]]
        meanings = meanings.union(extras)

    return meanings


def get_meanings_controller(
    acronyms_dict: AcronymsDict,
    language: Optional[str],
    category: Optional[str],
    name: Optional[str],
) -> Tuple[str, Set[str], str, str]:
    """Get the meanings CLI controller, it returns an acronym meaning with
    specific given parameters. If there are no language and no category,
    they will be selected randomly, same behavior for the name.

    Args:
        acronyms_dict (AcronymsDict): Every acronyms dict.
        language (Optional[str]): The optional acronym language
        category (Optional[str]): The optional acronym category
        name (Optional[str]): The acronym name

    Raises:
        PycronymsError: It has found zero acronyms
        PycronymsError: Wrong paramaters.
        PycronymsError: Missing acronym with a given name.

    Returns:
        Tuple[str, Set[str], str, str]: A tuple where each element respectively represent, acronym name, meanings, language, category.
    """

    if language and category:
        if not language in acronyms_dict:
            raise PycronymsError(f"The language {language} has zero acronyms.")

        categories_dict = acronyms_dict[language]
        if not category in categories_dict:
            raise PycronymsError(
                f"The category {category} with the langugage {language} has zero acronyms."
            )

        acronyms_dict = categories_dict[category]
    elif language is None and category is None:
        if name:
            raise PycronymsError(
                "The name parameter should not be used without the others."
            )

        language = random.choice(list(acronyms_dict.keys()))
        categories_dict = acronyms_dict[language]

        category = random.choice(list(categories_dict.keys()))
        acronyms_dict = categories_dict[category]
    else:
        raise PycronymsError(
            "When specyfing parameters, you must at least have language and category."
        )

    acronym_name: str
    if name is None:
        acronym_name = random.choice(list(acronyms_dict.keys()))
    else:
        name = name.upper()

        if not name in acronyms_dict:
            raise PycronymsError(
                f"The acronym '{name}' has not been fetched "
                f"with the language '{language}' "
                f"and the category '{category}'."
            )

        acronym_name = name.upper()

    acronym_dict = acronyms_dict[acronym_name]
    meanings = get_meanings(acronym_dict)

    return acronym_name, meanings, language, category


def guess_meanings(
    name: str, meanings: Set[str], language: str, category: str
) -> NoReturn:
    """Guess game run loop.

    Args:
        name (str): The acronym name
        meanings (Set[str]): The acronym meanings.
        language (str): The acronym language.
        category (str): The acronym category.
    """

    total_amount = len(meanings)

    print(
        f"The acronym '{name}' has {len(meanings)} meanings "
        f"with the language '{language}' "
        f"and the category '{category}'.\n"
        "To leave the guessing game, write 'quit'"
    )

    print()

    while meanings:
        meaning = input(f"Guess the meaning of '{name}'> ")

        if meaning == "quit":
            print()
            print(f"The following meanings were missing.")

            for meaning in meanings:
                print("-", meaning)

            return

        matched_meaning, score = process.extractOne(meaning, meanings)
        if score < 90:
            print(f"Incorrect, '{meaning}' is not a meaning of the acronym '{name}'.")
            continue

        meanings.remove(matched_meaning)

        missing_meanings_amount = len(meanings)

        print()
        print(f"Correct, '{matched_meaning}' is a meaning of the acronym '{name}'.")

        if missing_meanings_amount > 0:
            print(f"{missing_meanings_amount} remaining.")
            print()

    print(
        f"Congratulation, you found the {total_amount} meanings of the acronym {name}!"
    )


def main() -> NoReturn:
    """Guess game, the goal is to found the meaning of an selected acronym."""

    parser = create_parser()
    args = parser.parse_args()

    acronyms_dict = read_json_file(EMBEDDED_ACRONYMS_DIR / "all.json")

    name: str
    meanings: Set[str]
    language: str
    category: str

    try:
        name, meanings, language, category = get_meanings_controller(
            acronyms_dict, args.language, args.category, args.name
        )
    except PycronymsError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if len(meanings) == 0:
        print(f"There are no meanings for the acronym {name}", file=sys.stderr)
        sys.exit(1)

    guess_meanings(name, meanings, language, category)
