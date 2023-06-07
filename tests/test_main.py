import unittest
from unittest import mock
from src.setlist_builder import SetlistBuilder
from src.main import *


class TestSetlistBuilder(unittest.TestCase):
    """ class docstring """
    template_loc = 'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\setlist_template.json'
    track_list_loc = 'C:\\Users\Sierra\\Projects\\pound-setlist-generator\src\\track_list.json'

    def test_handle_track_replacement(self):
        """ method docstring """
        mock_setlist_builder = mock.Mock()
        attributes = {'difficulty':'beginner','length':'15','version':'a','include_arm_track':True,
         'template_location':self.template_loc,'songs_location':self.track_list_loc}
        mock_setlist_builder.configure_mock(**attributes)
        mock_setlist = []
        handle_track_replacement(mock_setlist_builder, 1, mock_setlist)





if __name__ == '__main__':
    unittest.main()