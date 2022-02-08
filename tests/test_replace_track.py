import unittest
import copy

from src.main import replace_track

class TestReplaceTrack(unittest.TestCase):
    def test_replace_warmup(self):
        setlist = [
            {
                'type':'warmup',
                'name':'Chains',
                'artist':'Nick Jonas'
            },
            {
                'type':'set',
                'level':'1',
                'name':'All Shook Up',
                'artist':'Whissell'
            },
            {
                'type':'kit',
                'level':'2',
                'name':'Dragula',
                'artist':'Rob Zombie'
            },
            {
                'type':'lunge',
                'level':'1',
                'name':'Teeth',
                'artist':'5 Seconds of Summer'
            },
            {
                'type':'cooldown',
                'name':'Feel It Still',
                'artist':'Portugal. The Man (Lido Remix)'
            }
        ]
        original_setlist = copy.deepcopy(setlist)
        replace_track(1, setlist)

        self.assertNotEqual(original_setlist[0], setlist[0])
        self.assertEqual(original_setlist[0]['type'], setlist[0]['type'])
        self.assertNotEqual(original_setlist[0]['name'], setlist[0]['name'])
        self.assertNotEqual(original_setlist[0]['artist'], setlist[0]['artist'])

        # replaced track is not the same as any other tracak in selist
        self.assertTrue(setlist[0] not in original_setlist)

    def test_replace_second_track(self):
        setlist = [
            {
                'type':'warmup',
                'name':'Chains',
                'artist':'Nick Jonas'
            },
            {
                'type':'set',
                'level':'1',
                'name':'All Shook Up',
                'artist':'Whissell'
            },
            {
                'type':'kit',
                'level':'2',
                'name':'Dragula',
                'artist':'Rob Zombie'
            },
            {
                'type':'lunge',
                'level':'1',
                'name':'Teeth',
                'artist':'5 Seconds of Summer'
            },
            {
                'type':'cooldown',
                'name':'Feel It Still',
                'artist':'Portugal. The Man (Lido Remix)'
            }
        ]

        original_setlist = copy.deepcopy(setlist)
        replace_track(2, setlist)

        # replaced track is not the same as before
        self.assertNotEqual(original_setlist[1], setlist[1])
        self.assertEqual(original_setlist[1]['type'], setlist[1]['type'])
        self.assertEqual(original_setlist[1]['level'], setlist[1]['level'])
        self.assertNotEqual(original_setlist[1]['name'], setlist[1]['name'])
        self.assertNotEqual(original_setlist[1]['artist'], setlist[1]['artist'])

        # replaced track is not the same as any other tracak in selist
        self.assertTrue(setlist[1] not in original_setlist)

