# import unittest

# from src.main import build_setlist

# class TestBuildSetlist(unittest.TestCase):
#     def test_build_beginner_15_a(self):
#         actual = build_setlist('beginner', '15', 'a')
#         self.assertEqual(len(actual), 5)
#         self.assertEqual(actual[0]['type'], 'warmup')
#         self.assertEqual(actual[1]['type'], 'set')
#         self.assertEqual(actual[1]['level'], '1')
#         self.assertEqual(actual[2]['type'], 'kit')
#         self.assertEqual(actual[2]['level'], '2')
#         self.assertEqual(actual[3]['type'], 'lunge')        
#         self.assertEqual(actual[3]['level'], '1')
#         self.assertEqual(actual[4]['type'], 'cooldown')
        

#     def test_build_advanced_45_b(self):
#         actual = build_setlist('beginner', '45', 'a')
#         self.assertEqual(len(actual), 12)
#         self.assertEqual(actual[0]['type'], 'warmup')
#         self.assertEqual(actual[1]['type'], 'set')
#         self.assertEqual(actual[1]['level'], '1')
#         self.assertEqual(actual[2]['type'], 'lunge')
#         self.assertEqual(actual[2]['level'], '1')
#         self.assertEqual(actual[3]['type'], 'kit')
#         self.assertEqual(actual[3]['level'], '1')
#         self.assertEqual(actual[4]['type'], 'set')        
#         self.assertEqual(actual[4]['level'], '1')
#         self.assertEqual(actual[5]['type'], 'lunge')
#         self.assertEqual(actual[5]['level'], '1')
#         self.assertEqual(actual[6]['type'], 'set')
#         self.assertEqual(actual[6]['level'], '2')
#         self.assertEqual(actual[7]['type'], 'kit')
#         self.assertEqual(actual[7]['level'], '1')
#         self.assertEqual(actual[8]['type'], 't&a')
#         self.assertEqual(actual[8]['level'], '1')
#         self.assertEqual(actual[9]['type'], 'set')
#         self.assertEqual(actual[9]['level'], '1')
#         self.assertEqual(actual[10]['type'], 'set')
#         self.assertEqual(actual[10]['level'], '3')
#         self.assertEqual(actual[11]['type'], 'cooldown')
        
#         for track in actual:
#             self.assertEqual(actual.count(track), 1)

# if __name__ == '__main__':
#     unittest.main()