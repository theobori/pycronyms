import os
import orjson
import logging
import sys
import random

from typing import NoReturn, Any, Optional, Tuple, Set
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path

from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.exceptions import PycronymsError
from pycronyms.acronyms import AcronymsDict, Acronyms
from pycronyms.acronym import Acronym
from pycronyms._common import create_recursive_dict

from pycronyms.cli.pycronyms_generate import OUTPUT_DIRNAME

from thefuzz import process

logger = logging.getLogger(__file__)

BASE_DIRPATH = Path(os.path.dirname(__file__))
EMBEDDED_ACRONYMS_DIR = BASE_DIRPATH / ".." / OUTPUT_DIRNAME


def create_subparser_guess(
    subparsers: "_SubParsersAction[ArgumentParser]",
) -> ArgumentParser:
    """Creating a subparser for the guess subcommand.

    Returns:
        ArgumentParser: The created parser.
    """

    parser = subparsers.add_parser("guess", help="Guess acronym meanings.")

    parser.add_argument(
        "-l",
        "--language",
        required=False,
        default=None,
        type=str,
        choices=Language._member_map_.values(),
    )
    parser.add_argument(
        "-c",
        "--category",
        required=False,
        default=None,
        type=str,
        choices=Category._member_map_.values(),
    )
    parser.add_argument("-n", "--name", required=False, default=None, type=str)

    parser.add_argument(
        "-d",
        "--dir",
        required=False,
        default=EMBEDDED_ACRONYMS_DIR,
        type=Path,
    )

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


def get_metadatas(
    acronyms: Acronyms,
    language: Optional[Language],
    category: Optional[Category],
    name: Optional[str],
) -> Tuple[str, Set[str], str, str]:
    """Get the acronym metadatas, it returns an acronym meaning with
    specific given parameters. If there are no language and no category,
    they will be selected randomly, same behavior for the name.

    Args:
        acronyms (AcronymsDict): Every acronyms dict.
        language (Optional[Language]): The optional acronym language
        category (Optional[Category]): The optional acronym category
        name (Optional[str]): The optional acronym name

    Raises:
        PycronymsError: It has found zero acronyms
        PycronymsError: Wrong paramaters.
        PycronymsError: Missing acronym with a given name.

    Returns:
        Tuple[str, Set[str], str, str]: A tuple where each element respectively represent, acronym name, meanings, language, category.
    """

    if language and category:
        if not language in acronyms:
            raise PycronymsError(f"The language {language} has zero acronyms.")

        categories = acronyms[language]
        if not category in categories:
            raise PycronymsError(
                f"The category {category} with the langugage {language} has zero acronyms."
            )

        acronyms = categories[category]
    elif language is None and category is None:
        if name:
            raise PycronymsError(
                "The name parameter should not be used without the others."
            )

        language = random.choice(list(acronyms))
        categories = acronyms[language]

        category = random.choice(list(categories))
        acronyms = categories[category]
    else:
        raise PycronymsError(
            "When specyfing parameters, you must at least have language and category."
        )

    acronym_name: str
    if name is None:
        acronym_name = random.choice(list(acronyms))
    else:
        name = name.upper()

        if not name in acronyms:
            raise PycronymsError(
                f"The acronym '{name}' has not been fetched "
                f"with the language '{language}' "
                f"and the category '{category}'."
            )

        acronym_name = name.upper()

    acronym: Acronym = acronyms[acronym_name]
    meanings = acronym.get_meanings()

    return acronym_name, meanings, language, category


def guess_meanings(
    name: str, meanings: Set[str], language: Language, category: Category
) -> NoReturn:
    """Guess game run loop.

    Args:
        name (str): The acronym name
        meanings (Set[str]): The acronym meanings.
        language (Language): The acronym language.
        category (Category): The acronym category.
    """

    total_amount = len(meanings)

    print(
        f"The acronym '{name}' has {len(meanings)} meanings "
        f"with the language '{language.iso_639_1_code}' "
        f"and the category '{category.value}'.\n"
        "To leave the guessing game, write 'quit'"
    )

    print()

    while meanings:
        meaning = input(f"Guess the meaning of '{name}'> ")

        if len(meaning) == 0:
            continue

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


def get_acronyms_from_json_path(path: Path) -> Acronyms:
    """Build a dict of acronyms with language and category.

    Args:
        path (Path): The directory path.

    Returns:
        Acronyms: The acronyms.
    """

    acronyms_dict: AcronymsDict = read_json_file(path)

    acronyms: Acronyms = create_recursive_dict(Acronym, 3)

    for lk, lv in acronyms_dict.items():
        for ck, cv in lv.items():
            for acronym_name, d in cv.items():
                d["name"] = acronym_name

                acronym = Acronym.from_dict(d)

                l = Language._value2member_map_[lk]
                c = Category._value2member_map_[ck]

                acronyms[l][c][acronym_name] = acronym

    return acronyms


def guess(
    iso_639_1_code: Optional[str], category_str: Optional[str], name: str, dir: Path
) -> NoReturn:
    """Guess game, the goal is to found the meaning of an selected acronym.

    Args:
        iso_639_1_code (str): The language code.
        category_str (str): The category as string/
        name (str): The acronym name.
        dir (Path): The output directory.
    """

    language = (
        None if iso_639_1_code is None else Language._value2member_map_[iso_639_1_code]
    )
    category = (
        None if category_str is None else Category._value2member_map_[category_str]
    )

    acronyms: Acronyms
    meanings: Set[str]
    try:
        acronyms = get_acronyms_from_json_path(dir / "all.json")

        name, meanings, language, category = get_metadatas(
            acronyms, language, category, name
        )
    except (PycronymsError, Exception) as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if len(meanings) == 0:
        print(f"There are no meanings for the acronym {name}", file=sys.stderr)
        sys.exit(1)

    guess_meanings(name, meanings, language, category)
