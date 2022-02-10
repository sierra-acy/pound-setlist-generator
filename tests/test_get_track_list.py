# import unittest

# from src.main import get_track_list

# class TestGetTracklist(unittest.TestCase):
#     def test_get_kit_1(self):
#         expected = [
#             {
#                 'name':'Crushcrushcrush',
#                 'artist':'Paramore'
#             },
#             {
#                 'name':'Come Out and Play',
#                 'artist':'The Offspring'
#             }
#         ]
#         actual = get_track_list('kit', '1')

#         self.assertEqual(expected, actual)
        
#     def test_get_TA_2(self):
#         expected = [
#             {
#                 'name':'Jimmy Shake',
#                 'artist':'740 Boyz, Apashe & Dose'
#             }
#         ]

#         actual = get_track_list('T&A','2')

#         self.assertEqual(expected, actual)

#     def test_get_cooldown(self):
#         expected = [
#             {
#                 'name':'Thank U Next',
#                 'artist':'Ariana Grande'
#             },
#             {
#                 'name':'Feel It Still',
#                 'artist':'Portugal. The Man (Lido Remix)'
#             },
#             {
#                 'name':'This is Halloween (Trap City Remix)',
#                 'artist':'Trap City'
#             }
#         ]

#         actual = get_track_list('cooldown', None)
#         self.assertEqual(expected, actual)

#     def test_get_bad_track_type(self):
#         self.assertRaises(Exception, get_track_list, 'type', '1')
        
#     def test_get_bad_level(self):
#         self.assertRaises(Exception, get_track_list, 'lunge', 'level')


# if __name__ == '__main__':
#     unittest.main()