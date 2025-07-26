from enum import IntEnum


class Language(IntEnum):
    """Represents a language."""

    ENGLISH = 0
    FRENCH = 1
    SPANISH = 2
    GERMAN = 3
    ITALIAN = 4
    PORTUGUESE = 5
    RUSSIAN = 6
    CHINESE = 7
    JAPANESE = 8
    ARABIC = 9

    # Using the enum values
    __iso_639_1_map = {
        ENGLISH: "en",
        FRENCH: "fr",
        SPANISH: "es",
        GERMAN: "de",
        ITALIAN: "it",
        PORTUGUESE: "pt",
        RUSSIAN: "ru",
        CHINESE: "zh",
        JAPANESE: "ja",
        ARABIC: "ar",
    }

    # Using the enum values
    __iso_639_1_map_vk = {v: k for k, v in __iso_639_1_map.items()}

    @property
    @staticmethod
    def default() -> "Language":
        return Language.ENGLISH

    @property
    def iso_639_1_code(self) -> str:
        return Language.__iso_639_1_map[self.value]

    @staticmethod
    def from_iso_639_1_code(code: str) -> "Language":
        """Returns a Language enum member from a ISO 639-1 string code

        Args:
            code (str): The code.

        Returns:
            Language: The enum member object.
        """

        if not code in Language.__iso_639_1_map_vk:
            return Language.default

        value = Language.__iso_639_1_map_vk[code]

        return Language._value2member_map_[value]
