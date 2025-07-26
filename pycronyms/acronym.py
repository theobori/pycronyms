from typing import Set, Any, Self

from pycronyms._common import normalize_str, remove_parenthesis_content

from pydantic import BaseModel, model_validator, Field


def is_acronym_meaning_valid(acronym: str, meaning: str) -> bool:
    acronym = acronym.strip().upper()
    meaning = meaning.strip()

    acronym_len = len(acronym)
    meaning_len = len(meaning)

    fi = i = 0
    while i < meaning_len and fi < acronym_len:
        # Check for successive uppercase
        if meaning[i].isupper() is True:
            while (
                i < meaning_len
                and meaning[i].isupper() is True
                and meaning[i] == acronym[fi]
            ):
                fi += 1
                i += 1
        # Otherwise we consider that only the first letter of the word should match
        elif meaning[i].upper() == acronym[fi].upper():
            fi += 1
            i += 1

        # Go to the next non-alphanumeric character
        while i < meaning_len and meaning[i].isalnum() is True:
            i += 1

        # Handling special cases like '/'
        if i < meaning_len and fi < acronym_len and acronym[fi] == meaning[i]:
            fi += 1

        # Skip the non-alphanumeric character to go on a word letter or number
        i += 1

    return fi >= acronym_len


class Acronym(BaseModel):
    """This model represents an acronym."""

    name: str = Field(min_length=2)  # Assuming an acronym has at least two characters
    meaning: str = Field(
        min_length=5
    )  # Assuming its meaning has at least two words, and a word being at least two letters and a separator
    provider: str = Field(min_length=1, default="unknown")
    extras: Set["Acronym"] = set()

    def __hash__(self):
        return hash(self.name + "__" + self.meaning)

    def model_post_init(self, _context: Any):
        """Post initialization for normalizing strings"""

        self.meaning = remove_parenthesis_content(self.meaning)

        for attr, attr_value in vars(self).items():
            if isinstance(attr_value, str) is False:
                continue

            normalized_attr = normalize_str(attr_value)
            setattr(self, attr, normalized_attr)

        # Remove every whitespace character
        self.name = "".join(self.name.split()).upper()

    @model_validator(mode="after")
    def check_meaning(self) -> Self:
        if is_acronym_meaning_valid(self.name, self.meaning) is False:
            raise ValueError(
                f"The meaning {self.meaning} does not match the acronym {self.name}"
            )

        return self
