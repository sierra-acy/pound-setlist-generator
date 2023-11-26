import unittest
from cmdline.pound_setlist_builder import PoundSetlistBuilder

class TestPoundSetlistBuilder(unittest.TestCase):
    """ Tests PoundSetlistBuilder Class """
    
    template_name = 'pound_setlist_template.json'
    track_list_name = 'pound_track_list.json'

    # input: difficulty, length, version, inlcude_arm_track, template_name, track_list_name
    # output: vars set to each of above, template
    def test_init_pound_setlist_builder(self):
        """ Test PoundSetlistBuilder constructor """

        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', True, self.template_name, self.track_list_name)

        self.assertEqual(pound_setlist_builder.get_difficulty(), 'beginner')
        self.assertEqual(pound_setlist_builder.get_length(), '15')
        self.assertEqual(pound_setlist_builder.get_version(), 'a')
        self.assertEqual(pound_setlist_builder.get_include_arm_track(), True)

    ### PARSE SETLIST TEMPLATE ###
    def test_parse_beginner_15_a_template(self):
        """ Test _parse_pound_setlist_template with beginner setlist """
        
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
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        actual = pound_setlist_builder._parse_pound_setlist_template(self.template_name)

        self.assertEqual(expected, actual)
        
    def test_parse_advanced_45_b_template(self):
        """ Test _parse_pound_setlist_template with advanced setlist in caps """
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
        pound_setlist_builder = PoundSetlistBuilder('Advanced', '45', 'B', False, self.template_name, self.track_list_name)
        actual = pound_setlist_builder._parse_pound_setlist_template(self.template_name)

        self.assertEqual(expected, actual)

    ### BUILD SETLIST ###
    def test_build_setlist_beginner_15_a(self):
        """ Test build_setlist"""
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        # pound_setlist_builder._parse_pound_setlist_template(self.template_name)
        setlist = pound_setlist_builder.build_setlist()

        template = pound_setlist_builder.get_template()
        self.assertEqual(len(pound_setlist_builder.get_template()), len(setlist))
        for slot, track in zip(template, setlist):
            self.assertEqual(slot['type'], track['type'])
            if 'level' in slot:
                self.assertTrue('level' in track)
                self.assertTrue(slot['level'], track['level'])

    def test_build_setlist_beginner_30_a_arm(self):
        """ Test build_setlist"""
        pound_setlist_builder = PoundSetlistBuilder('beginner', '30', 'a', True, self.template_name, self.track_list_name)
        # pound_setlist_builder._parse_pound_setlist_template(self.template_name)
        setlist = pound_setlist_builder.build_setlist()

        template = pound_setlist_builder.get_template()
        self.assertEqual(len(pound_setlist_builder.get_template()), len(setlist))
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
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        setlist = pound_setlist_builder.build_setlist()
        new_track = pound_setlist_builder._build_new_track(setlist, track_template)
        self.assertEqual(new_track['type'], track_template['type'])
        self.assertEqual(new_track['level'], track_template['level'])
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
        pound_setlist_builder = PoundSetlistBuilder('beginner', '30', 'a', True, self.template_name, self.track_list_name)
        setlist = pound_setlist_builder.build_setlist()
        new_track = pound_setlist_builder._build_new_track(setlist, track_template)
        self.assertEqual(new_track['type'], track_template['type'])
        self.assertEqual(new_track['level'], track_template['level'])
        self.assertIsNotNone(new_track['name'])
        self.assertIsNotNone(new_track['artist'])
        self.assertTrue(new_track['isArmTrack'])

    def test_build_new_track_no_level(self):
        """ Test building track with no level """
        track_template = {
                    "type":"warmup"
                }
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        setlist = pound_setlist_builder.build_setlist()
        new_track = pound_setlist_builder._build_new_track(setlist, track_template)
        self.assertEqual(new_track['type'], track_template['type'])
        self.assertIsNone(new_track['level'])
        self.assertIsNotNone(new_track['name'])
        self.assertIsNotNone(new_track['artist'])
        self.assertFalse(new_track['isArmTrack'])

    ### PARSE TRACK LIST ###
    def test_parse_pound_track_list(self):
        """ Test parsing track list from JSON file to JSON object """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        pound_track_list = pound_setlist_builder._parse_pound_track_list('lunge', '2')
        self.assertTrue(len(pound_track_list) > 0)
        single_track = pound_track_list[0]
        self.assertIsNotNone(single_track['name'])
        self.assertIsNotNone(single_track['artist'])
        self.assertIsNotNone(single_track['canBeArmTrack'])

    ### AUTO REPLACE TRACK ###
    def test_auto_replace_cooldown(self):
        """ Test auto_replace_track with cooldown """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        # pound_setlist_builder._parse_pound_setlist_template(self.template_name)
        setlist = pound_setlist_builder.build_setlist()
        old_cooldown_track = setlist[4]
        setlist = pound_setlist_builder.auto_replace_track(setlist, '5')
        new_cooldown_track = setlist[4]

        self.assertNotEqual(old_cooldown_track, new_cooldown_track)
        self.assertEqual(new_cooldown_track['type'], 'cooldown')

    def test_auto_replace_arm_track(self):
        """ Test auto_replace_track with lunge """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '30', 'a', True, self.template_name, self.track_list_name)
        # pound_setlist_builder._parse_pound_setlist_template(self.template_name)
        setlist = pound_setlist_builder.build_setlist()
        old_track = setlist[5]
        setlist = pound_setlist_builder.auto_replace_track(setlist, '6')
        new_track = setlist[5]

        self.assertNotEqual(old_track, new_track)
        self.assertEqual(old_track['type'], new_track['type'])
        self.assertEqual(old_track['level'], new_track['level'])
        self.assertTrue(new_track['isArmTrack'])

    ### GET REPLACEMENT TRACK OPTIONS ###
    def test_get_replacement_options(self):
        """ Test getting replacement options for regular track """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        setlist = pound_setlist_builder.build_setlist()
        track_options = pound_setlist_builder.get_replacement_track_options(setlist, '2')
        old_track = setlist[1]

        full_list = pound_setlist_builder._parse_pound_track_list(old_track['type'], old_track['level'])
        for option in track_options:
            this_track = {'name': option['name'], 'artist': option['artist'], 'canBeArmTrack': option['canBeArmTrack']}
            self.assertTrue(this_track in full_list)

    def test_get_replacement_options_arm(self):
        """ Test getting replacement options for arm track """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '45', 'a', True, self.template_name, self.track_list_name)
        setlist = pound_setlist_builder.build_setlist()
        track_options = pound_setlist_builder.get_replacement_track_options(setlist, '10')
        old_track = setlist[9]

        full_list = pound_setlist_builder._parse_pound_track_list(old_track['type'], old_track['level'])
        for option in track_options:
            this_track = {'name': option['name'], 'artist': option['artist'], 'canBeArmTrack': option['canBeArmTrack']}
            self.assertTrue(this_track in full_list)

    def test_get_replacement_options_no_level(self):
        """ Test getting replacement options for track with no level """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        setlist = pound_setlist_builder.build_setlist()
        track_options = pound_setlist_builder.get_replacement_track_options(setlist, '1')
        old_track = setlist[0]
        
        full_list = pound_setlist_builder._parse_pound_track_list(old_track['type'], old_track['level'])
        for option in track_options:
            this_track = {'name': option['name'], 'artist': option['artist'], 'canBeArmTrack': option['canBeArmTrack']}
            self.assertTrue(this_track in full_list)

    ### REPLACE TRACK ###
    def test_replace_track(self):
        """ Test replace_track """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '30', 'a', False, self.template_name, self.track_list_name)
        # pound_setlist_builder._parse_pound_setlist_template(self.template_name)
        setlist = pound_setlist_builder.build_setlist()

        track_options = pound_setlist_builder.get_replacement_track_options(setlist, '2')
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

        pound_setlist_builder.replace_track(setlist, '2', new_track)
        self.assertEqual(setlist[1]['name'], new_track['name'])
        self.assertEqual(setlist[1]['artist'], new_track['artist'])        
        self.assertFalse(setlist[1]['isArmTrack'])

    def test_replace_arm_track(self):
        """ Test replace arm track """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '45', 'a', True, self.template_name, self.track_list_name)
        # pound_setlist_builder._parse_pound_setlist_template(self.template_name)
        setlist = pound_setlist_builder.build_setlist()
        track_options = pound_setlist_builder.get_replacement_track_options(setlist, '10')
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

        pound_setlist_builder.replace_track(setlist, '10', new_track)
        self.assertEqual(setlist[9]['name'], new_track['name'])
        self.assertEqual(setlist[9]['artist'], new_track['artist'])        
        self.assertTrue(setlist[9]['isArmTrack'])

    def test_replace_track_no_level(self):
        """ Test replace_track no level """
        pound_setlist_builder = PoundSetlistBuilder('beginner', '15', 'a', False, self.template_name, self.track_list_name)
        setlist = pound_setlist_builder.build_setlist()
        track_options = pound_setlist_builder.get_replacement_track_options(setlist, '1')
        old_track = setlist[0]
        new_track = track_options[0]
        self.assertTrue(new_track['name'] != old_track['name'] or new_track['artist'] != old_track['artist'])


        setlist = pound_setlist_builder.replace_track(setlist, '1', new_track)
        self.assertEqual(setlist[0]['name'], new_track['name'])
        self.assertEqual(setlist[0]['artist'], new_track['artist'])
        self.assertFalse(setlist[0]['isArmTrack'])

if __name__ == '__main__':
    unittest.main()