import unittest

from src.main import get_setlist_template

class TestTemplateLoad(unittest.TestCase):
    def test_get_beginner_15_a(self):
        expected = [
            {
                'type': 'warmup'
            },
            {
                'type': 'set',
                'level': 1
            },
            {
                'type': 'kit',
                'level': 2
            },
            {
                'type': 'lunge',
                'level': 1
            },
            {
                'type': 'cooldown'
            }
        ]
        actual = get_setlist_template("beginner","15", "a", "src/")

        self.assertEqual(expected, actual)
        
    def test_get_Advanced_45_B(self):
        expected = [
            {
                "type":"warmup"
            },
            {
                "type":"set",
                "level":1
            },
            {
                "type":"set",
                "level":2
            },
            {
                "type":"kit",
                "level":1
            },
            {
                "type":"lunge",
                "level":1
            },
            {
                "type":"set",
                "level":3
            },
            {
                "type":"set",
                "level":2
            },
            {
                "type":"kit",
                "level":2
            },
            {
                "type":"t&a",
                "level":2
            },
            {
                "type":"set",
                "level":1,
                "canBeArmTrack":True
            },
            {
                "type":"lunge",
                "level":2
            },
            {
                "type":"cooldown"
            }
        ]

        actual = get_setlist_template("Advanced","45", "B", "src/")

        self.assertEqual(expected, actual)

    def test_get_bad_path(self):
        self.assertRaises(FileNotFoundError, get_setlist_template, "advanced", "45", "b", "path")

    def test_get_bad_difficulty(self):
        self.assertRaises(KeyError, get_setlist_template, "difficulty", "45", "b", "src/")
    
    def test_get_bad_length(self):
        self.assertRaises(KeyError, get_setlist_template, "advanced", "length", "b", "src/")
        
    def test_get_bad_version(self):
        self.assertRaises(KeyError, get_setlist_template, "advanced", "45", "version", "src/")

if __name__ == "__main__":
    unittest.main()