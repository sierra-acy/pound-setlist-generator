import json
import random

class PomSetlistBuilder:
    """" Builds and maintains setlist """

    def __init__(self, length, template_location, songs_location):
        """ stores the setlist length and initializes template and empty setlist"""
        self.length = length
        self.template = self._parse_pom_setlist_template(template_location)
        self.songs_location = './src/json/' + songs_location

    def build_setlist(self):
        """ Creates setlist for current template and vars """
        setlist = []
        for slot in self.template:
            setlist_track = self._build_new_track(setlist, slot)
            setlist.append(setlist_track)
        return setlist
    
    def get_replacement_track_options(self, setlist, track_num):
        """ Gets list of tracks with same params as given track_num """
        # get old track details
        track_index = int(track_num) - 1
        old_track = setlist[track_index]
        track_type = old_track['type']
    
        # get user choice  
        track_options = self._parse_pom_track_list(track_type)

        # filter duplicates
        track_options = list(filter(lambda track, track_type=track_type: {"name":track['name'], "artist":track['artist'], "type":track_type} not in setlist, track_options))

        return track_options
    
    def replace_track(self, setlist, replace_track_num, new_track):
        """ Replaces given track with given new track in setlist """
        track_index = int(replace_track_num) - 1
        old_track = setlist[track_index]
        track_type = old_track['type']

        insert = {}
        insert['type'] = track_type
        insert['name'] = new_track['name']
        insert['artist'] = new_track['artist']

        setlist[track_index] = insert
        return setlist
    
    def auto_replace_track(self, setlist, track_num):
        """ Automatically replaces specified track with random track of same type """
        track_index = int(track_num) - 1
        new_track = self._build_new_track(setlist, self.template[track_index])

        setlist[track_index] = new_track
        return setlist
        
    def _parse_pom_setlist_template(self, template_location):
        """ Transform setlist from JSON file text to JSON object as global var """

        with open('./src/json/' + template_location, 'r') as template_file:
            data = template_file.read()
            data_json = json.loads(data)
            template = data_json[self.length]
            return template
        
    def _parse_pom_track_list(self, track_type):
        """ Transforms known tracks from JSON file text to JSON object """
        with open(self.songs_location, 'r') as pom_track_list_file:
            data = pom_track_list_file.read()
            data_json = json.loads(data)
            try:
                pom_track_list = data_json[str(track_type)]
            except KeyError:
                raise Exception(f'No track of type {track_type} available in list of known songs. Please choose a different setlist or update the song list.')
        
            return pom_track_list
    
    def _build_new_track(self, setlist, track_template):
        """ Chooses and builds a single setlist track after filtering for dupes and requirements"""
        track_type = track_template['type']
        track_options = self._parse_pom_track_list(track_type)

        track_options = list(filter(lambda track, track_type=track_type: {"name":track['name'], "artist":track['artist'], "type":track_type} not in setlist, track_options))

        if len(track_options) == 0:
                raise Exception(f'No tracks available of type {track_type} for slot {track_template}."')
    
        chosen_track = track_options[random.randrange(0, len(track_options))]
        
        new_track = {}
        new_track['type'] = track_type
        new_track['name'] = chosen_track['name']
        new_track['artist'] = chosen_track['artist']

        return new_track
        
    def get_length(self):
        """ length global var getter """
        return self.length
    
    def get_template(self):
        """ template global var getter """
        return self.template