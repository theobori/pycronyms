from typing import NoReturn
from pathlib import Path

from pycronyms.handler_acronyms import HandlerAcronyms
from pycronyms.acronyms import Acronyms, create_acronyms
from pycronyms.acronym import Acronym
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms.exceptions import HandlerError

import pandas as pd


class HandlerCSV(HandlerAcronyms):
    """CSV acronyms handler. It reads and writes CSV files."""

    name = "csv"
    columns = ("name", "language", "category", "provider", "meaning")

    @classmethod
    def read(cls, filepath: Path) -> Acronyms:
        """Read a CSV file then get a Acronyms Python object with its content.

        Args:
            filepath (Path): The source CSV file path.

        Raises:
            HandlerError: An error occured when reading the CSV filepath.

        Returns:
            Acronyms: The acronyms.
        """

        acronyms = create_acronyms()

        df: pd.DataFrame
        try:
            df = pd.read_csv(filepath)
        except Exception as e:
            raise HandlerError(cls.name, filepath) from e

        for _, row in df.iterrows():
            name, language, category, provider, meaning = list(row)

            acronym = Acronym(name=name, meaning=meaning, provider=provider)

            language = Category._value2member_map_[language]
            category = Category._value2member_map_[category]

            entry = acronyms[language][category]

            if name in entry:
                entry[name].add_extra(acronym)
            else:
                entry[name] = acronym

        return acronyms

    @classmethod
    def write(cls, filepath: Path, data: Acronyms) -> NoReturn:
        """Write to a CSV file from a Acronyms Python object.

        Args:
            filepath (Path): The destination CSV file path.
            data (Acronyms): Acronyms to override the content to write to the file.

        Raises:
            HandlerError: An error occured when writting to the CSV file.
        """

        df_data = {col: [] for col in cls.columns}

        def append_acronym(acronym: Acronym, language: Language, category: Category):
            df_data["name"].append(acronym.name)
            df_data["language"].append(language.iso_639_1_code)
            df_data["category"].append(category.value)
            df_data["provider"].append(acronym.provider)
            df_data["meaning"].append(acronym.meaning)

        for language, lv in data.items():
            for category, cv in lv.items():
                for _, acronym in cv.items():
                    append_acronym(acronym, language, category)

                    for extra in acronym.extras:
                        append_acronym(extra, language, category)

        df = pd.DataFrame(df_data, columns=cls.columns)

        try:
            df.to_csv(filepath, index=False, header=True)
        except Exception as e:
            raise HandlerError(cls.name, filepath) from e
