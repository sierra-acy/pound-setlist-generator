import unittest

from src.setlist_builder import SetlistBuilder

class TestSetlistBuilder(unittest.TestCase):
    """ Tests SetlistBuilder Class """
        
    def test_create_setlist_builder(self):
        """ Test SetlistBuilder constructor """
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        self.assertEqual(setlist_builder.get_difficulty(), 'beginner')
        self.assertEqual(setlist_builder.get_length(), '15')
        self.assertEqual(setlist_builder.get_version(), 'a')

    ### PARSE SETLIST TEMPLATE ###
    def test_parse_beginner_15_a_template(self):
        """ Test _parse_setlist_template with beginner setlist """
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
        
    def test_parse_advanced_45_b_template(self):
        """ Test _parse_setlist_template with advanced setlist in caps """
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
        """ Test build_setlist"""
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

    ### AUTO REPLACE TRACK ###
    def test_auto_replace_cooldown(self):
        """ Test auto_replace_track with cooldown """
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        old_cooldown_track = setlist[4]
        setlist = setlist_builder.auto_replace_track('5')
        new_cooldown_track = setlist[4]

        self.assertNotEqual(old_cooldown_track, new_cooldown_track)
        self.assertEqual(new_cooldown_track['type'], 'cooldown')

    def test_auto_replace_lunge_1(self):
        """ Test auto_replace_track with lunge """
        setlist_builder = SetlistBuilder('beginner', '15', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        old_lunge_track = setlist[3]
        setlist = setlist_builder.auto_replace_track('4')
        new_lunge_track = setlist[3]

        self.assertNotEqual(old_lunge_track, new_lunge_track)
        self.assertEqual(old_lunge_track['type'], new_lunge_track['type'])
        self.assertEqual(old_lunge_track['level'], new_lunge_track['level'])
    
    ### NEW TRACK IS DUPLICATE ###
    def test_new_track_is_duplicate_true(self):
        """ Test new_track_is_duplicate with duplicate """
        setlist_builder = SetlistBuilder('beginner', '30', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('2')

        old_track = {}
        old_track['name'] = setlist[1]['name']
        old_track['artist'] = setlist[1]['artist']

        if old_track not in list(track_options):
            old_track['canBeArmTrack'] = True
            
        new_track = track_options[list(track_options).index(old_track)]

        actual = setlist_builder.new_track_is_duplicate(new_track, '2')
        self.assertEqual(True, actual)

    def test_new_track_is_duplicate_false(self):
        """ Test new_track_is_duplicate with no dupe """
        setlist_builder = SetlistBuilder('beginner', '30', 'a')
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('2')

        old_track = {}
        old_track['name'] = setlist[1]['name']
        old_track['artist'] = setlist[1]['artist']

        old_track_with_arm = {}
        old_track_with_arm['name'] = setlist[1]['name']
        old_track_with_arm['artist'] = setlist[1]['artist']
        old_track_with_arm['canBeArmTrack'] = True
        
        found = False
        i = 0
        while not found:
            if track_options[i] != old_track and track_options[i] != old_track_with_arm:
                found = True
            else:
                i += 1
        new_track = track_options[i]
        
        actual = setlist_builder.new_track_is_duplicate(new_track, '2')
        self.assertEqual(False, actual)

    ### REPLACE TRACK ###
    def test_replace_track(self):
        """ Test replace_track """
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