import json
import random

class SetlistBuilder:
    """ SetlistBuilder handles all setlist state changes """
    def __init__(self, difficulty, length, version):
        """ init stores difficulty, length, version, 
        initializes template, and initializes empty setlist"""
        self.difficulty = str(difficulty).lower()
        self.length = str(length).lower()
        self.version = str(version).lower()
        self.template = self._parse_setlist_template()
        self.setlist = []
        
    def _parse_setlist_template(self):
        """ Transform setlist from JSON file text to JSON object as global var """
        template = None
        with open('src/setlist_template.json', 'r') as template_file:
            data = template_file.read()
            data_json = json.loads(data)
            template = data_json[self.difficulty][self.length][self.version]
        template_file.close()
        return template

    def build_setlist(self):
        """ Creates setlist for current template and vars """
        for slot in self.template:
            track_type = slot['type']
            track_level = None
            if 'level' in slot:
                track_level = slot['level']
            
            track_list = self._parse_track_list(track_type, track_level)

            # choose random track and ensure no duplicates
            duplicate_track = True
            setlist_track = None
            while duplicate_track:
                track_index = random.randrange(0, len(track_list))
                chosen_track = track_list[track_index]

                setlist_track = {}
                setlist_track['type'] = track_type
                if track_level is not None:
                    setlist_track['level'] = track_level
                setlist_track['name'] = chosen_track['name']
                setlist_track['artist'] = chosen_track['artist']

                if(setlist_track not in self.setlist):
                    duplicate_track = False
            self.setlist.append(setlist_track)
        return self.setlist
    
    def _parse_track_list(self, track_type, track_level):
        """ Transforms known tracks from JSON file text to JSON object """
        track_list = None
        with open('src/track_list.json', 'r') as track_list_file:
            data = track_list_file.read()
            data_json = json.loads(data)
            try:
                track_list = data_json[track_type]
            except KeyError:
                track_list_file.close()
                raise Exception(f'No track of type {track_type} available in list of known songs. Please choose a different setlist or update the song list.')

            if track_level:
                try:
                    track_list = track_list[track_level]
                except KeyError:
                    track_list_file.close()
                    raise Exception(f'No track of type {track_type} with level {track_level} available in list of known songs. Please choose a different setlist or update the song list.')

        track_list_file.close()
        return track_list

    def print_setlist(self):
        """ Print setlist in numbered order """
        for index, track in enumerate(self.setlist):
            track_type = str(track['type']).capitalize()
            track_name = track['name']
            track_artist = track['artist']
            if 'level' in track:
                track_level = track['level']
                print(f'{index+1}. {track_type} Level {track_level} - {track_name} by {track_artist}')
            else:
                print(f'{index+1}. {track_type} - {track_name} by {track_artist}')

    def auto_replace_track(self, track_num):
        """ Automatically replaces specified track with random track of same type """
        track_index = int(track_num) - 1
        old_track = self.setlist[track_index]
        track_type = old_track['type']
        track_level = None
        if 'level' in old_track:
            track_level = old_track['level']

        duplicate = True
        new_track = None
        while duplicate:
            track_list = self._parse_track_list(track_type, track_level)
            chosen_track_index = random.randrange(0, len(track_list))
            chosen_track = track_list[chosen_track_index]

            new_track = {}
            new_track['type'] = track_type
            if track_level:
                new_track['level'] = track_level
            new_track['name'] = chosen_track['name']
            new_track['artist'] = chosen_track['artist']

            if new_track != old_track and new_track not in self.setlist:
                duplicate = False
        self.setlist[track_index] = new_track
        return self.setlist

    def get_replacement_track_options(self, track_num):
        """ Gets list of tracks with same params as given track_num """
        # get old track details
        track_index = int(track_num) - 1
        old_track = self.setlist[track_index]
        track_type = old_track['type']

        if 'level' in old_track:
            track_level = old_track['level']
        else:
            track_level = None

        # get user choice  
        track_list = self._parse_track_list(track_type, track_level)
        return track_list
    
    def new_track_is_duplicate(self, track, old_track_num):
        """ Returns true if track is the same as the old track
        or as another track in the setlist """
        old_track_index = int(old_track_num) - 1
        old_track = self.setlist[old_track_index]
        # build new track object
        new_track = {}
        new_track['type'] = old_track['type']
        if 'level' in old_track:
            new_track['level'] = old_track['level']
        new_track['name'] = track['name']
        new_track['artist'] = track['artist']

        # check for duplicates
        # TODO: check for duplicates excluding track being replaced
        # TODO: check for choosing same song as replacing
        if new_track in self.setlist:
            return True
        return False

    def replace_track(self, replace_track_num, new_track):
        """ Replaces given track with given new track in setlist """
        track_index = int(replace_track_num) - 1
        old_track = self.setlist[track_index]
        track_type = old_track['type']
        track_level = None
        if 'level' in old_track:
            track_level = old_track['level']

        insert = {}
        insert['type'] = track_type
        if track_level:
            insert['level'] = track_level
        insert['name'] = new_track['name']
        insert['artist'] = new_track['artist']

        self.setlist[track_index] = insert
        return self.setlist 

    def get_difficulty(self):
        """ difficulty global var getter """
        return self.difficulty
    
    def get_length(self):
        """ length global var getter """
        return self.length

    def get_version(self):
        """ version global var getter """
        return self.version

    def get_setlist(self):
        """ setlist global var getter """
        return self.setlist

    def get_template(self):
        """ template global var getter """
        return self.template