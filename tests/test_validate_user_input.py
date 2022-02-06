import unittest

from src.main import validate_user_input

class TestValidateUserInput(unittest.TestCase):

    def test_beginner_15_a(self):
        self.assertEqual(validate_user_input('beginner', '15', 'a'), True)

    def test_cap_params(self):
        self.assertEqual(validate_user_input('Beginner', '15', 'A'), True)

    def test_bad_difficulty(self):
        self.assertEqual(validate_user_input('difficulty', '15', 'a'), False)

    def test_bad_length(self):
        self.assertEqual(validate_user_input('beginner', 'length', 'a'), False)

    def test_bad_version(self):
        self.assertEqual(validate_user_input('beginner', '15', 'version'), False)

if __name__ == '__main__':
    unittest.main()