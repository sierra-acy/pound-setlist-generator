import unittest
from src.setlist_builder import SetlistBuilder

class TestGetTemplate(unittest.TestCase):
    def test_get_beginner_15_a(self):
        expected = [
            {
                'type': 'warmup'
            },
            {
                'type': 'set',
                'level': '1'
            },
            {
                'type': 'kit',
                'level': '2'
            },
            {
                'type': 'lunge',
                'level': '1'
            },
            {
                'type': 'cooldown'
            }
        ]
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        actual = setlist_builder.get_setlist_template()

        self.assertEqual(expected, actual)
        
    def test_get_Advanced_45_B(self):
        expected = [
            {
                'type':'warmup'
            },
            {
                'type':'set',
                'level':'1'
            },
            {
                'type':'set',
                'level':'2'
            },
            {
                'type':'kit',
                'level':'1'
            },
            {
                'type':'lunge',
                'level':'1'
            },
            {
                'type':'set',
                'level':'3'
            },
            {
                'type':'set',
                'level':'2'
            },
            {
                'type':'kit',
                'level':'2'
            },
            {
                'type':'t&a',
                'level':'2'
            },
            {
                'type':'set',
                'level':'1',
                'canBeArmTrack':True
            },
            {
                'type':'lunge',
                'level':'2'
            },
            {
                'type':'cooldown'
            }
        ]
        setlist_builder = SetlistBuilder('Advanced', '45', 'B')
        actual = setlist_builder.get_setlist_template()

        self.assertEqual(expected, actual)

    # def test_get_bad_difficulty(self):
    #     setlist_builder = SetlistBuilder('difficuly', '45', 'b')
    #     self.assertRaises(KeyError, setlist_builder.get_setlist_template, 'difficulty', '45', 'b')
    
    # def test_get_bad_length(self):
    #     self.assertRaises(KeyError, get_setlist_template, 'advanced', 'length', 'b')
        
    # def test_get_bad_version(self):
    #     self.assertRaises(KeyError, get_setlist_template, 'advanced', '45', 'version')

if __name__ == '__main__':
    unittest.main()