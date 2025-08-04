import sys

from typing import NoReturn
from argparse import ArgumentParser

from pycronyms.cli.pycronyms_generate import generate, create_subparser_generate
from pycronyms.cli.pycronyms_guess import guess, create_subparser_guess


def create_parser() -> ArgumentParser:
    """Creating a parser.

    Returns:
        ArgumentParser: The created parser.
    """

    parser = ArgumentParser(description="The pycronyms CLI.")

    return parser


def main() -> NoReturn:
    """Pycronyms CLI entry point."""

    parser = create_parser()

    subparsers = parser.add_subparsers(dest="subparser_name")

    create_subparser_guess(subparsers)
    create_subparser_generate(subparsers)

    args = parser.parse_args()

    subparser_name = args.subparser_name

    match subparser_name:
        case "generate":
            generate(args.dir)
        case "guess":
            guess(args.language, args.category, args.name, args.dir)
