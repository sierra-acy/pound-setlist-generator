import unittest
from src.pom_setlist_builder import PomSetlistBuilder

class TestPoundSetlistBuilder(unittest.TestCase):
    """ Tests PoundSetlistBuilder Class """

    # template_loc = 'C:\\Users\Sierra\\Projects\\pom-setlist-generator\src\json\pom_setlist_template.json'
    # pound_track_list_loc = 'C:\\Users\Sierra\\Projects\\pom-setlist-generator\src\json\\pom_track_list.json'
    template_name = 'pom_setlist_template.json'
    track_list_name = 'pom_track_list.json'

    # input: length, template_loc, pound_track_list_loc
    # output: vars set to each of above, template
    def test_init_pound_setlist_builder(self):
        """ Test PoundSetlistBuilder constructor """

        pom_setlist_builder = PomSetlistBuilder('30', self.template_name, self.track_list_name)
        self.assertEqual(pom_setlist_builder.get_length(), '30')

    def test_build_setlist(self):
        """ Test build_setlist"""
        pom_setlist_builder = PomSetlistBuilder('20', self.template_name, self.track_list_name)
        setlist = pom_setlist_builder.build_setlist()

        template = pom_setlist_builder.get_template()
        self.assertEqual(len(pom_setlist_builder.get_template()), len(setlist))
        for slot, track in zip(template, setlist):
            self.assertEqual(slot['type'], track['type'])

    def test_get_replacement_options(self):
        """ Test getting replacement options for regular track """
        pom_setlist_builder = PomSetlistBuilder('20', self.template_name, self.track_list_name)
        setlist = pom_setlist_builder.build_setlist()
        track_options = pom_setlist_builder.get_replacement_track_options(setlist, '2')
        old_track = setlist[1]

        full_list = pom_setlist_builder._parse_pom_track_list(old_track['type'])
        for option in track_options:
            this_track = {'name': option['name'], 'artist': option['artist']}
            self.assertTrue(this_track in full_list)

    def test_replace_track(self):
        """ Test replace_track """
        pom_setlist_builder = PomSetlistBuilder('20', self.template_name, self.track_list_name)
        setlist = pom_setlist_builder.build_setlist()

        track_options = pom_setlist_builder.get_replacement_track_options(setlist, '2')
        old_track = setlist[1]
        new_track = track_options[0]
        self.assertTrue(new_track['name'] != old_track['name'] or new_track['artist'] != old_track['artist'])

        pom_setlist_builder.replace_track(setlist, '2', new_track)
        self.assertEqual(setlist[1]['name'], new_track['name'])
        self.assertEqual(setlist[1]['artist'], new_track['artist'])        

    def test_auto_replace_cooldown(self):
        """ Test auto_replace_track with cooldown """
        pom_setlist_builder = PomSetlistBuilder('20', self.template_name, self.track_list_name)
        setlist = pom_setlist_builder.build_setlist()
        old_cooldown_track = setlist[4]
        setlist = pom_setlist_builder.auto_replace_track(setlist, '5')
        new_cooldown_track = setlist[4]

        self.assertNotEqual(old_cooldown_track, new_cooldown_track)
        self.assertEqual(new_cooldown_track['type'], 'cooldown')

    def test_parse_pom_setlist_template(self):
        """ Test _parse_pom_setlist_template with 30 min setlist """
        
        expected = [
            {
                "type":"warmup"
            },
            {
                "type":"prancing"
            },
            {
                "type": "standard"
            },
            {
                "type": "standard"
            },
            {
                "type": "standard"
            },
            {
                "type":"kick"
            },
            {
                "type":"cooldown"
            }
        ]
        pom_setlist_builder = PomSetlistBuilder('30', self.template_name, self.track_list_name)
        actual = pom_setlist_builder._parse_pom_setlist_template(self.template_name)

        self.assertEqual(expected, actual)

    def test_parse_pom_track_list(self):
        """ Test parsing track list from JSON file to JSON object """
        pom_setlist_builder = PomSetlistBuilder('20', self.template_name, self.track_list_name)
        pom_track_list = pom_setlist_builder._parse_pom_track_list('standard')
        self.assertTrue(len(pom_track_list) > 0)
        single_track = pom_track_list[0]
        self.assertIsNotNone(single_track['name'])
        self.assertIsNotNone(single_track['artist'])

    def test_build_new_track_standard(self):
        """ Test building regular track """
        track_template = { "type":"standard" }
        pom_setlist_builder = PomSetlistBuilder('20', self.template_name, self.track_list_name)
        setlist = pom_setlist_builder.build_setlist()
        new_track = pom_setlist_builder._build_new_track(setlist, track_template)
        self.assertEqual(new_track['type'], track_template['type'])
        self.assertIsNotNone(new_track['name'])
        self.assertIsNotNone(new_track['artist'])
    

if __name__ == '__main__':
    unittest.main()