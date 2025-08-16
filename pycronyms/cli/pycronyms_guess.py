import os
import logging
import sys
import random

from typing import NoReturn, Optional, Tuple, Set
from argparse import ArgumentParser, _SubParsersAction
from pathlib import Path

from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.exceptions import PycronymsError
from pycronyms.acronyms import Acronyms
from pycronyms.acronym import Acronym
from pycronyms.handlers import HandlerJSON

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
) -> bool:
    """Guess game run loop. Returns false if the user has left.

    Args:
        name (str): The acronym name
        meanings (Set[str]): The acronym meanings.
        language (Language): The acronym language.
        category (Category): The acronym category.

    Returns:
        bool: Guess game state.
    """

    total_amount = len(meanings)

    while meanings:
        meaning = input(
            f"('{language.iso_639_1_code}', '{category.fancy_value()}') Guess the meaning of '{name}'> "
        )

        if len(meaning) == 0:
            continue

        c = meaning in {"continue", "c"}

        if meaning in {"quit", "q"} or c:
            print()
            print(f"The following meanings were missing.")

            for meaning in meanings:
                print("-", meaning)

            print()

            return c

        matched_meaning, score = process.extractOne(meaning, meanings)
        if score < 96:
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

    return True


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

    user_name = name
    user_language = (
        None if iso_639_1_code is None else Language._value2member_map_[iso_639_1_code]
    )
    user_category = (
        None if category_str is None else Category._value2member_map_[category_str]
    )

    try:
        acronyms = HandlerJSON.read(dir / "all.json")

        print(
            "To leave the guessing game, write 'quit' or 'q', to continue write 'continue' or 'c'."
        )

        print()

        run = True
        while run:
            name, meanings, language, category = get_metadatas(
                acronyms, user_language, user_category, user_name
            )

            if len(meanings) == 0:
                raise PycronymsError(f"There are no meanings for the acronym {name}")

            del acronyms[language][category][name]

            run = guess_meanings(name, meanings, language, category)
            if user_name and run:
                break
    except (PycronymsError, Exception) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
