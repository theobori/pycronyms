from enum import StrEnum


class Category(StrEnum):
    """Represents a category."""

    COMMON = "common"
    COMPUTER_SCIENCE = "computer_science"

    def fancy_value(self) -> str:
        return self.value.replace("_", " ").title()
