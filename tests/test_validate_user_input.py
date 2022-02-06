import unittest

from src.main import validate_user_input

class TestValidateUserInput(unittest.TestCase):

    def test_beginner_15_a(self):
        self.assertTrue(validate_user_input('beginner', '15', 'a'))

    def test_cap_params(self):
        self.assertTrue(validate_user_input('Beginner', '15', 'A'))

    def test_bad_difficulty(self):
        self.assertFalse(validate_user_input('difficulty', '15', 'a'))

    def test_bad_length(self):
        self.assertFalse(validate_user_input('beginner', 'length', 'a'))

    def test_bad_version(self):
        self.assertFalse(validate_user_input('beginner', '15', 'version'))

if __name__ == '__main__':
    unittest.main()