from typing import Dict, NoReturn, Optional

import pandas as pd
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt

from pycronyms._common import create_recursive_dict
from pycronyms.language import Language
from pycronyms.category import Category
from pycronyms._common import get_current_date


class Statistics:
    """This object is used to count the acronyms with multiple point of view."""

    def __init__(self, filepath_csv: Optional[Path] = None):
        # Assuming this fields will never be updated from outside the object
        self.language_and_category: Dict[Language, Dict[Category, int]] = (
            create_recursive_dict(int, depth=2)
        )
        self.language: Dict[Language, int] = defaultdict(int)
        self.category: Dict[Category, int] = defaultdict(int)
        self.total = 0

        self.filepath_csv = filepath_csv

    def increase(self, language: Language, category: Category, amount: int):
        """Increase the amount of acronyms.

        Args:
            language (Language): The language.
            category (Category): The category.
            amount (int): The amount to add.
        """

        self.language_and_category[language][category] += amount
        self.language[language] += amount
        self.category[category] += amount
        self.total += amount

    @property
    def dataframe(self) -> pd.DataFrame:
        """Returns a pandas dataframe representing the acronyms statistics.
        It implies the CSV filepath if there is one.

        Returns:
            pd.DataFrame: A pandas dataframe.
        """

        data = {}
        data["date"] = [get_current_date()]
        data["total"] = [self.total]

        for language in Language:
            data[language.value] = [self.language[language]]

        df = pd.DataFrame(data)

        if self.filepath_csv and self.filepath_csv.exists():
            df_csv = pd.read_csv(self.filepath_csv)

            row = df.loc[0]

            if list(df_csv.loc[len(df_csv) - 1]) != list(row):
                df_csv.loc[-1] = row

            df = df_csv

        return df

    def append_to_csv(self) -> NoReturn:
        """Append a row to a CSV file with a given file location.
        The row represents the statistics.
        """

        df = self.dataframe

        if self.filepath_csv:
            df.to_csv(self.filepath_csv, index=False, header=True)

    def create_plot(self, filepath: Path) -> NoReturn:
        """Create and write to a PNG file a plot. The data is the statistics
        per language and total.

        Args:
            filepath (Path): The file path.
        """

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        df = self.dataframe
        x = df["date"]

        ax1.set_title("Evolution of the amount of acronyms per language")

        for l in Language:
            y = df[l.value]
            ax1.plot(x, y, label=l.value, marker="o")

        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Number of acronyms")

        ax2.set_title("Evolution of the total amount of acronyms")

        y = df["total"]
        ax2.plot(x, y, label="total", marker="o")

        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Total number of acronyms")

        plt.tight_layout()

        fig.savefig(filepath, dpi=300, bbox_inches="tight")
        plt.close()
