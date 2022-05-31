import unittest

from src.setlist_builder import SetlistBuilder

class TestSetlistBuilder(unittest.TestCase):
    """ Tests SetlistBuilder Class """
        
    template_loc = 'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json'
    track_list_loc = 'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json'

    def test_create_setlist_builder(self):
        """ Test SetlistBuilder constructor """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', True, self.template_loc, self.track_list_loc)
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
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        actual = setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')

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
        setlist_builder = SetlistBuilder('Advanced', '45', 'B', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        actual = setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')

        self.assertEqual(expected, actual)

    ### BUILD SETLIST ###
    def test_build_setlist_beginner_15_a(self):
        """ Test build_setlist"""
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        # setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')
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
        setlist_builder = SetlistBuilder('beginner', '30', 'a', True, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        # setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')
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

    ### BUILD NEW TRACK ###
    def test_build_new_track_regular(self):
        """ Test building regular track """
        track_template = {
                    "type":"set",
                    "level":"1"
                }
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', '../src/track_list.json')
        setlist = setlist_builder.build_setlist()
        new_track = setlist_builder._build_new_track(setlist, track_template)
        self.assertEquals(new_track['type'], track_template['type'])
        self.assertEquals(new_track['level'], track_template['level'])
        self.assertIsNotNone(new_track['name'])
        self.assertIsNotNone(new_track['artist'])
        self.assertFalse(new_track['isArmTrack'])

    def test_build_new_track_arm(self):
        """ Test building arm track """
        track_template = {
                    "type":"set",
                    "level":"1",
                    "canBeArmTrack":True
                }
        setlist_builder = SetlistBuilder('beginner', '30', 'a', True, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', '../src/track_list.json')
        setlist = setlist_builder.build_setlist()
        new_track = setlist_builder._build_new_track(setlist, track_template)
        self.assertEquals(new_track['type'], track_template['type'])
        self.assertEquals(new_track['level'], track_template['level'])
        self.assertIsNotNone(new_track['name'])
        self.assertIsNotNone(new_track['artist'])
        self.assertTrue(new_track['isArmTrack'])

    def test_build_new_track_no_level(self):
        """ Test building track with no level """
        track_template = {
                    "type":"warmup"
                }
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', '../src/track_list.json')
        setlist = setlist_builder.build_setlist()
        new_track = setlist_builder._build_new_track(setlist, track_template)
        self.assertEquals(new_track['type'], track_template['type'])
        self.assertIsNone(new_track['level'])
        self.assertIsNotNone(new_track['name'])
        self.assertIsNotNone(new_track['artist'])
        self.assertFalse(new_track['isArmTrack'])

    ### PARSE TRACK LIST ###
    def test_parse_track_list(self):
        """ Test parsing track list from JSON file to JSON object """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        track_list = setlist_builder._parse_track_list('lunge', '2')
        self.assertTrue(len(track_list) > 0)
        single_track = track_list[0]
        self.assertIsNotNone(single_track['name'])
        self.assertIsNotNone(single_track['artist'])
        self.assertIsNotNone(single_track['canBeArmTrack'])

    ### AUTO REPLACE TRACK ###
    def test_auto_replace_cooldown(self):
        """ Test auto_replace_track with cooldown """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        # setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')
        setlist = setlist_builder.build_setlist()
        old_cooldown_track = setlist[4]
        setlist = setlist_builder.auto_replace_track(setlist, '5')
        new_cooldown_track = setlist[4]

        self.assertNotEqual(old_cooldown_track, new_cooldown_track)
        self.assertEqual(new_cooldown_track['type'], 'cooldown')

    def test_auto_replace_arm_track(self):
        """ Test auto_replace_track with lunge """
        setlist_builder = SetlistBuilder('beginner', '30', 'a', True, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        # setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')
        setlist = setlist_builder.build_setlist()
        old_track = setlist[5]
        setlist = setlist_builder.auto_replace_track(setlist, '6')
        new_track = setlist[5]

        self.assertNotEqual(old_track, new_track)
        self.assertEqual(old_track['type'], new_track['type'])
        self.assertEqual(old_track['level'], new_track['level'])
        self.assertTrue(new_track['isArmTrack'])

    ### GET REPLACEMENT TRACK OPTIONS ###
    def test_get_replacement_options(self):
        """ Test getting replacement options for regular track """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options(setlist, '2')
        old_track = setlist[1]
        for option in track_options:
            self.assertEqual(option['type'], old_track['type'])
            self.assertEqual(option['level'], old_track['level'])
            self.assertTrue(option['name'] != old_track['name'] or option['artist'] != old_track['artist'])
            self.assertEqual(option['isArmTrack'], old_track['isArmTrack'])

    def test_get_replacement_options_arm(self):
        """ Test getting replacement options for arm track """
        setlist_builder = SetlistBuilder('beginner', '45', 'a', True, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options(setlist, '10')
        old_track = setlist[9]
        for option in track_options:
            self.assertEqual(option['type'], old_track['type'])
            self.assertEqual(option['level'], old_track['level'])
            self.assertTrue(option['name'] != old_track['name'] or option['artist'] != old_track['artist'])
            self.assertTrue(option['isArmTrack'])

    def test_get_replacement_options_no_level(self):
        """ Test getting replacement options for track with no level """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options(setlist, '1')
        old_track = setlist[0]
        for option in track_options:
            self.assertEqual(option['type'], old_track['type'])
            self.assertIsNone(option['level'])
            self.assertTrue(option['name'] != old_track['name'] or option['artist'] != old_track['artist'])
            self.assertEqual(option['isArmTrack'], old_track['isArmTrack'])

    ### REPLACE TRACK ###
    def test_replace_track(self):
        """ Test replace_track """
        setlist_builder = SetlistBuilder('beginner', '30', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        # setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')
        setlist = setlist_builder.build_setlist()

        track_options = setlist_builder.get_replacement_track_options(setlist, '2')
        old_track = setlist[1]
        new_track = track_options[0]
        self.assertTrue(new_track['name'] != old_track['name'] or new_track['artist'] != old_track['artist'])

        # found = False
        # i = 0
        # while not found:
        #     if track_options[i] != old_track:
        #         found = True
        #     else:
        #         i += 1
        # new_track = track_options[i]

        setlist_builder.replace_track(setlist, '2', new_track)
        self.assertEqual(setlist[1]['name'], new_track['name'])
        self.assertEqual(setlist[1]['artist'], new_track['artist'])        
        self.assertFalse(setlist[1]['isArmTrack'])

    def test_replace_arm_track(self):
        """ Test replace arm track """
        setlist_builder = SetlistBuilder('beginner', '45', 'a', True, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        # setlist_builder._parse_setlist_template(r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json')
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options(setlist, '10')
        old_track = setlist[9]
        new_track = track_options[0]
        self.assertTrue(new_track['name'] != old_track['name'] or new_track['artist'] != old_track['artist'])

        # old_track = {}
        # old_track['name'] = setlist[1]['name']
        # old_track['artist'] = setlist[1]['artist']
        
        # found = False
        # i = 0
        # while not found:
        #     if track_options[i] != old_track and track_options[i]['canBeArmTrack']:
        #         found = True
        #     elif i == len(track_options):
        #         old_name = old_track['name']
        #         raise Exception(f'Arm track {old_name} cannot be replaced with a new arm track because it is the only arm track available in the list of track options: {track_options}')
        #     else:
        #         i += 1
        # new_track = track_options[i]

        setlist_builder.replace_track(setlist, '10', new_track)
        self.assertEqual(setlist[9]['name'], new_track['name'])
        self.assertEqual(setlist[9]['artist'], new_track['artist'])        
        self.assertTrue(setlist[9]['isArmTrack'])

    def test_replace_track_no_level(self):
        """ Test replace_track no level """
        setlist_builder = SetlistBuilder('beginner', '15', 'a', False, r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json', r'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json')
        setlist = setlist_builder.build_setlist()
        track_options = setlist_builder.get_replacement_track_options(setlist, '1')
        old_track = setlist[0]
        new_track = track_options[0]
        self.assertTrue(new_track['name'] != old_track['name'] or new_track['artist'] != old_track['artist'])


        setlist = setlist_builder.replace_track(setlist, '1', new_track)
        self.assertEqual(setlist[0]['name'], new_track['name'])
        self.assertEqual(setlist[0]['artist'], new_track['artist'])
        self.assertFalse(setlist[0]['isArmTrack'])

if __name__ == '__main__':
    unittest.main()