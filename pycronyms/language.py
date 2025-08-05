from enum import StrEnum


class Language(StrEnum):
    """Represents a language with ISO 639-1 code as value"""

    ENGLISH = "en"
    FRENCH = "fr"
    SPANISH = "es"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    ARABIC = "ar"

    @property
    @staticmethod
    def default() -> "Language":
        return Language.ENGLISH

    @property
    def iso_639_1_code(self) -> str:
        return self.value
