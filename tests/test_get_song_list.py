import unittest

from src.main import get_song_list

class TestTemplateLoad(unittest.TestCase):
    def test_get_kit_1(self):
        expected = [
            {
                'name':'Crushcrushcrush',
                'artist':'Paramore'
            },
            {
                'name':'Come Out and Play',
                'artist':'The Offspring'
            }
        ]
        actual = get_song_list('kit', '1', 'src/')

        self.assertEqual(expected, actual)
        
    def test_get_TA_2(self):
        expected = [
            {
                'name':'Jimmy Shake',
                'artist':'740 Boyz, Apashe & Dose'
            }
        ]

        actual = get_song_list('T&A','2', 'src/')

        self.assertEqual(expected, actual)

    def test_get_cooldown(self):
        expected = [
            {
                'name':'Thank U Next',
                'artist':'Ariana Grande'
            },
            {
                'name':'Feel It Still',
                'artist':'Portugal. The Man (Lido Remix)'
            },
            {
                'name':'This is Halloween (Trap City Remix)',
                'artist':'Trap City'
            }
        ]

        actual = get_song_list('cooldown', None, 'src/')
        self.assertEqual(expected, actual)

    def test_get_bad_path(self):
        self.assertRaises(FileNotFoundError, get_song_list, 'set', '3', 'path')

    def test_get_bad_track_type(self):
        self.assertRaises(KeyError, get_song_list, 'type', '1', 'src/')
    
    def test_get_bad_level(self):
        self.assertRaises(KeyError, get_song_list, 'lunge', 'level', 'src/')

if __name__ == '__main__':
    unittest.main()