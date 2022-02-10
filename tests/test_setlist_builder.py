import unittest

from src.setlist_builder import SetlistBuilder

class TestSetlistBuilder(unittest.TestCase):
        
    def test_create_setlist_builder(self):
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        self.assertEqual(setlist_builder.get_difficulty(), 'beginner')
        self.assertEqual(setlist_builder.get_length(), '15')
        self.assertEqual(setlist_builder.get_version(), 'a')

    ### PARSE SETLIST TEMPLATE ###
    def test_parse_beginner_15_a_template(self):
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
        actual = setlist_builder._parse_setlist_template()

        self.assertEqual(expected, actual)
        
    def test_parse_Advanced_45_B_template(self):
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
        actual = setlist_builder._parse_setlist_template()

        self.assertEqual(expected, actual)

    ### BUILD SETLIST ###
    def test_build_setlist_beginner_15_a(self):
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()

        template = setlist_builder.get_template()
        self.assertEqual(len(setlist_builder.get_template()), len(setlist))
        for slot, track in zip(template, setlist):
            self.assertEqual(slot['type'], track['type'])
            if 'level' in slot:
                self.assertTrue('level' in track)
                self.assertTrue(slot['level'], track['level'])

    ### PARSE TRACK LIST ###
    # def test_parse_track_list_set_2(self):
    #     setlist_builder = SetlistBuilder('beginner', '15', 'a')
    #     track_list = setlist_builder._parse_track_list('set', '2')
        
    #     self.assertTrue(len(track_list) >= 1)
    #     for track in track_list:
    #         self.assertEqual(track['type'], 'set')
    #         self.assertEqual(track['level'], '2')

    # def test_parse_track_list_warmup(self):
    #     setlist_builder = SetlistBuilder('beginner', '15', 'a')
    #     track_list = setlist_builder._parse_track_list('warmup', None)
        
    #     self.assertTrue(len(track_list) >= 1)
    #     for track in track_list:
    #         self.assertEqual(track['type'], 'warmup')
    #         self.assertFalse('level' in track)

    ### AUTO REPLACE TRACK ###
    def test_auto_replace_cooldown(self):
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        old_cooldown_track = setlist[4]
        setlist = setlist_builder.auto_replace_track('5')
        new_cooldown_track = setlist[4]

        self.assertNotEqual(old_cooldown_track, new_cooldown_track)
        self.assertEqual(new_cooldown_track['type'], 'cooldown')

    def test_auto_replace_lunge_1(self):
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        old_lunge_track = setlist[3]
        setlist = setlist_builder.auto_replace_track('4')
        new_lunge_track = setlist[3]

        self.assertNotEqual(old_lunge_track, new_lunge_track)
        self.assertEqual(old_lunge_track['type'], new_lunge_track['type'])
        self.assertEqual(old_lunge_track['level'], new_lunge_track['level'])

    ### GET REPLACEMENT TRACK OPTIONS ###
    # def test_replacement_track_options_set_1(self):
    #     setlist_builder = SetlistBuilder('beginner', '15', 'a')
    #     setlist_builder._parse_setlist_template()
    #     setlist = setlist_builder.build_setlist()
    #     original_track = setlist[1]
    #     track_options = setlist_builder.get_replacement_track_options('2')

    #     for track in track_options:
    #         print(original_track)
    #         print(track)
    #         self.assertEqual(original_track['type'], track['type'])
    #         self.assertEqual(original_track['level'], track['level'])
    
    ### NEW TRACK IS DUPLICATE ###
    def test_new_track_is_duplicate_true(self):
        setlist_builder = SetlistBuilder('beginner', '30', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('2')

        old_track = {}
        old_track['name'] = setlist[1]['name']
        old_track['artist'] = setlist[1]['artist']
        
        new_track = track_options[list(track_options).index(old_track)]
        
        actual = setlist_builder.new_track_is_duplicate(new_track, '2')
        self.assertEqual(True, actual)

    def test_new_track_is_duplicate_false(self):
        setlist_builder = SetlistBuilder('beginner', '30', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('2')

        old_track = {}
        old_track['name'] = setlist[1]['name']
        old_track['artist'] = setlist[1]['artist']
        
        found = False
        i = 0
        while not found:
            if track_options[i] != old_track:
                found = True
            else:
                i += 1
        new_track = track_options[i]
        
        actual = setlist_builder.new_track_is_duplicate(new_track, '2')
        self.assertEqual(False, actual)

    ### REPLACE TRACK ###
    def test_replace_track(self):
        setlist_builder = SetlistBuilder('beginner', '30', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('2')

        old_track = {}
        old_track['name'] = setlist[1]['name']
        old_track['artist'] = setlist[1]['artist']
        
        found = False
        i = 0
        while not found:
            if track_options[i] != old_track:
                found = True
            else:
                i += 1
        new_track = track_options[i]

        setlist_builder.replace_track(2, new_track)

if __name__ == '__main__':
    unittest.main()