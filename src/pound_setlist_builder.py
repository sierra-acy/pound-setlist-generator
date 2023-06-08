import json
import random

class PoundSetlistBuilder:
    """ SetlistBuilder handles all setlist state changes """
    def __init__(self, difficulty, length, version, include_arm_track, template_location, songs_location):
        """ init stores difficulty, length, version, 
        initializes template, and initializes empty setlist"""
        self.difficulty = str(difficulty).lower()
        self.length = str(length).lower()
        self.version = str(version).lower()
        self.include_arm_track = include_arm_track
        self.template = self._parse_pound_setlist_template(template_location)
        self.songs_location = songs_location
        
    def _parse_pound_setlist_template(self, template_location):
        """ Transform setlist from JSON file text to JSON object as global var """

        with open(template_location, 'r') as template_file:
            data = template_file.read()
            data_json = json.loads(data)
            template = data_json[self.difficulty][self.length][self.version]
            return template

    def build_setlist(self):
        """ Creates setlist for current template and vars """
        setlist = []
        for slot in self.template:
            setlist_track = self._build_new_track(setlist, slot)
            setlist.append(setlist_track)
        return setlist
    
    def _build_new_track(self, setlist, track_template):
        """ Chooses and builds a single setlist track after filtering for dupes and requirements"""
        track_type = track_template['type']
        track_level = None
        if 'level' in track_template:
            track_level = track_template['level']
        track_options = self._parse_pound_track_list(track_type, track_level)

        is_arm_track = False
        if 'canBeArmTrack' in track_template and self.include_arm_track:
            track_options = list(filter(lambda track: track['canBeArmTrack'] is True, track_options))
            is_arm_track = True

        track_options = list(filter(lambda track, track_type=track_type, track_level=track_level, is_arm_track=is_arm_track: {"name":track['name'], "artist":track['artist'], "type":track_type, "level":track_level, "isArmTrack":is_arm_track} not in setlist, track_options))
        
        if len(track_options) == 0:
                raise Exception(f'No tracks available of type {track_type} with level {track_level} for slot {track_template}."')
    
        chosen_track = track_options[random.randrange(0, len(track_options))]
        
        new_track = {}
        new_track['type'] = track_type
        new_track['level'] = track_level
        new_track['name'] = chosen_track['name']
        new_track['artist'] = chosen_track['artist']
        new_track['isArmTrack'] = is_arm_track

        return new_track


    def _parse_pound_track_list(self, track_type, track_level):
        """ Transforms known tracks from JSON file text to JSON object """
        with open(self.songs_location, 'r') as pound_track_list_file:
            data = pound_track_list_file.read()
            data_json = json.loads(data)
            try:
                pound_track_list = data_json[str(track_type)]
            except KeyError:
                raise Exception(f'No track of type {track_type} available in list of known songs. Please choose a different setlist or update the song list.')

            if track_level:
                try:
                    pound_track_list = pound_track_list[str(track_level)]
                except KeyError:
                    raise Exception(f'No track of type {track_type} with level {track_level} available in list of known songs. Please choose a different setlist or update the song list.')
            return pound_track_list

    def auto_replace_track(self, setlist, track_num):
        """ Automatically replaces specified track with random track of same type """
        track_index = int(track_num) - 1
        new_track = self._build_new_track(setlist, self.template[track_index])

        setlist[track_index] = new_track
        return setlist

    def get_replacement_track_options(self, setlist, track_num):
        """ Gets list of tracks with same params as given track_num """
        # get old track details
        track_index = int(track_num) - 1
        old_track = setlist[track_index]
        track_type = old_track['type']
        track_level = old_track['level']
    
        # get user choice  
        track_options = self._parse_pound_track_list(track_type, track_level)
        is_arm_track = False
        if 'canBeArmTrack' in self.template[track_index] and self.include_arm_track:
            track_options = list(filter(lambda track: track['canBeArmTrack'] is True, track_options))
            is_arm_track = True

        # filter duplicates
        track_options = list(filter(lambda track, track_type=track_type, track_level=track_level, is_arm_track=is_arm_track: {"name":track['name'], "artist":track['artist'], "type":track_type, "level":track_level, "isArmTrack":is_arm_track} not in setlist, track_options))

        return track_options

    def replace_track(self, setlist, replace_track_num, new_track):
        """ Replaces given track with given new track in setlist """
        track_index = int(replace_track_num) - 1
        old_track = setlist[track_index]
        track_type = old_track['type']
        track_level = old_track['level']
        is_arm_track = old_track['isArmTrack']

        insert = {}
        insert['type'] = track_type
        insert['level'] = track_level
        insert['name'] = new_track['name']
        insert['artist'] = new_track['artist']
        insert['isArmTrack'] = is_arm_track

        setlist[track_index] = insert
        return setlist

    def get_difficulty(self):
        """ difficulty global var getter """
        return self.difficulty
    
    def get_length(self):
        """ length global var getter """
        return self.length

    def get_version(self):
        """ version global var getter """
        return self.version

    def get_include_arm_track(self):
        """ include arm track global var getter """
        return self.include_arm_track

    def get_template(self):
        """ template global var getter """
        return self.template