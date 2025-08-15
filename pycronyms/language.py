from enum import StrEnum


class Language(StrEnum):
    """Represents a language with ISO 639-1 code as value"""

    # Please keep this in order, only add entries to the end (bottom).
    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "es"
    GERMAN = "de"
    ITALIAN = "it"

    @property
    @staticmethod
    def default() -> "Language":
        return Language.ENGLISH

    @property
    def iso_639_1_code(self) -> str:
        return self.value
