import unittest

from src.setlist_builder import SetlistBuilder

class TestSetlistBuilder(unittest.TestCase):
    """ Tests SetlistBuilder Class """
        
    def test_create_setlist_builder(self):
        """ Test SetlistBuilder constructor """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', True)
        self.assertEqual(setlist_builder.get_difficulty(), 'beginner')
        self.assertEqual(setlist_builder.get_length(), '15')
        self.assertEqual(setlist_builder.get_version(), 'a')
        self.assertEqual(setlist_builder.get_include_arm_track(), True)

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
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False)
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
        setlist_builder = SetlistBuilder('Advanced', '45', 'B', False)
        actual = setlist_builder._parse_setlist_template()

        self.assertEqual(expected, actual)

    ### BUILD SETLIST ###
    def test_build_setlist_beginner_15_a(self):
        """ Test build_setlist"""
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False)
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()

        template = setlist_builder.get_template()
        self.assertEqual(len(setlist_builder.get_template()), len(setlist))
        for slot, track in zip(template, setlist):
            self.assertEqual(slot['type'], track['type'])
            if 'level' in slot:
                self.assertTrue('level' in track)
                self.assertTrue(slot['level'], track['level'])

    def test_build_setlist_beginner_30_a_arm(self):
        """ Test build_setlist"""
        setlist_builder = SetlistBuilder('beginner', '30', 'a', True)
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()

        template = setlist_builder.get_template()
        self.assertEqual(len(setlist_builder.get_template()), len(setlist))
        for slot, track in zip(template, setlist):
            self.assertEqual(slot['type'], track['type'])
            if 'level' in slot:
                self.assertTrue('level' in track)
                self.assertTrue(slot['level'], track['level'])    
            if 'canBeArmTrack' in slot:
                self.assertTrue(track['isArmTrack'])


    ### AUTO REPLACE TRACK ###
    def test_auto_replace_cooldown(self):
        """ Test auto_replace_track with cooldown """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False)
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        old_cooldown_track = setlist[4]
        setlist = setlist_builder.auto_replace_track('5')
        new_cooldown_track = setlist[4]

        self.assertNotEqual(old_cooldown_track, new_cooldown_track)
        self.assertEqual(new_cooldown_track['type'], 'cooldown')

    def test_auto_replace_arm_track(self):
        """ Test auto_replace_track with lunge """
        setlist_builder = SetlistBuilder('beginner', '30', 'a', True)
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        old_track = setlist[5]
        setlist = setlist_builder.auto_replace_track('6')
        new_track = setlist[5]

        self.assertNotEqual(old_track, new_track)
        self.assertEqual(old_track['type'], new_track['type'])
        self.assertEqual(old_track['level'], new_track['level'])
        self.assertTrue(new_track['isArmTrack'])

    
    ### NEW TRACK IS DUPLICATE ###
    def test_new_track_is_duplicate_true(self):
        """ Test new_track_is_duplicate with duplicate """
        setlist_builder = SetlistBuilder('beginner', '30', 'a', False)
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('2')
        setlist_builder.replace_track('2', track_options[0])

        actual = setlist_builder.new_track_is_duplicate(track_options[0], '6')
        self.assertEqual(True, actual)

    def test_new_track_is_duplicate_false(self):
        """ Test new_track_is_duplicate with no dupe """
        setlist_builder = SetlistBuilder('beginner', '30', 'a', False)
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('2')
        setlist[1] = track_options[0]
        
        actual = setlist_builder.new_track_is_duplicate(track_options[1], '6')
        self.assertEqual(False, actual)

    ### REPLACE TRACK ###
    def test_replace_track(self):
        """ Test replace_track """
        setlist_builder = SetlistBuilder('beginner', '30', 'a', False)
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

    def test_replace_arm_track(self):
        """ Test replace_track """
        setlist_builder = SetlistBuilder('beginner', '30', 'a', True)
        setlist_builder._parse_setlist_template()
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options('6')

        old_track = {}
        old_track['name'] = setlist[1]['name']
        old_track['artist'] = setlist[1]['artist']
        
        found = False
        i = 0
        while not found:
            if track_options[i] != old_track and track_options[i]['canBeArmTrack']:
                found = True
            elif i == len(track_options):
                old_name = old_track['name']
                raise Exception(f'Arm track {old_name} cannot be replaced with a new arm track because it is the only arm track available in the list of track options: {track_options}')
            else:
                i += 1
        new_track = track_options[i]

        setlist_builder.replace_track(6, new_track)

if __name__ == '__main__':
    unittest.main()