import unittest

from pycronyms.acronym import is_acronym_meaning_valid, Acronym

from pydantic import ValidationError

ACRONYM_MEANING_VALID = {
    "RADAR": "RAdio Detection And Ranging",
    "SHDSL": "Single-pair High-speed Digital Subscriber Line",
    "SED": "Self-encrypting drive",
    "SD": "Secure Digital",
    "S/MIME": "Secure/Multipurpose Internet Mail Extensions",
    "SQLi": "SQL injection",
    "lol": "lot of laugh",
    "USR": "U.S. Robotics",
    "UART": "Universal Asynchronous Receiver/Transmitter",
}

ACRONYM_MEANING_INVALID = {
    "RADAR": "RAdio And Ranging",
    "RADAR": "Radio Detection And Ranging",
    "SD": "SecureDigital",
    "lol": "lot laugh",
    "lol": " Lot Of aLaugh",
}


class TestAcronym(unittest.TestCase):
    """Controller for the acronym model and functions"""

    def test_meaning_validation(self):
        """Test if acronym meanings are valid"""

        for acronym, meaning in ACRONYM_MEANING_VALID.items():
            self.assertTrue(is_acronym_meaning_valid(acronym, meaning))

        for acronym, meaning in ACRONYM_MEANING_INVALID.items():
            self.assertFalse(is_acronym_meaning_valid(acronym, meaning))

    def test_acronym(self):
        """Tests with the acronym object model"""

        acronym_before_post_init = Acronym(
            name="  s d  ", meaning="   Secure       Digital  "
        )
        acronym_after_post_init = Acronym(name="SD", meaning="Secure Digital")
        self.assertEqual(acronym_before_post_init, acronym_after_post_init)

        with self.assertRaises(ValidationError):
            Acronym(name=" H W ", meaning="Hello zorld")


if __name__ == "__main__":
    unittest.main()
