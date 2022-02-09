
import json
import random

class SetlistBuilder:
    def __init__(self, difficulty, length, version):
        self.difficulty = str(difficulty).lower()
        self.length = str(length).lower()
        self.version = str(version).lower()
        self.template = self.get_setlist_template()
        self.setlist = []
        
    def get_setlist_template(self):
        template = None
        with open('src/setlist_template.json', 'r') as template_file:
            data = template_file.read()
            data_json = json.loads(data)
            template = data_json[self.difficulty][self.length][self.version]
        template_file.close()
        return template

    def build_setlist(self):
        for slot in self.template:
            track_type = slot['type']
            track_level = None
            if 'level' in slot:
                track_level = slot['level']
            
            track_list = self._get_track_list(track_type, track_level)

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
    
    def _get_track_list(self, track_type, track_level):
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
        for index, track in enumerate(self.setlist):
            track_type = str(track['type']).capitalize()
            track_name = track['name']
            track_artist = track['artist']
            if 'level' in track:
                track_level = track['level']
                print(f'{index+1}. {track_type} Level {track_level} - {track_name} by {track_artist}')
            else:
                print(f'{index+1}. {track_type} - {track_name} by {track_artist}')

    def replace_track(self, track_num):
        track_index = track_num - 1
        old_track = self.setlist[track_index]
        track_type = old_track['type']
        track_level = None
        if 'level' in old_track:
            track_level = old_track['level']

        duplicate = True
        new_track = None
        while duplicate:
            track_list = self._get_track_list(track_type, track_level)
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

    def get_difficulty(self):
        return self.difficulty
    
    def get_length(self):
        return self.length

    def get_version(self):
        return self.version
    

# def replace_track_user_choice(track_num, setlist):
#     # get old track details
#     track_index = track_num - 1
#     old_track = setlist[track_index]
#     track_type = old_track['type']

#     if 'level' in old_track:
#         track_level = old_track['level']
#     else:
#         track_level = None

#     # get user choice  
#     track_list = get_track_list(track_type, track_level)  
#     if track_level:
#         options = f'{str(track_type).capitalize()} level {track_level} tracks:\n'
#     else:
#         options = f'{str(track_type).capitalize()} tracks:\n'

#     for index, track in enumerate(track_list):
#         name = track['name']
#         artist = track['artist']
#         options += f'{index+1}. {name} by {artist}\n'
#     print(options)
#     replace_with_choice = None
#     while replace_with_choice not in range(1, len(track_list)+1):
#         try:
#             old_name = old_track['name']
#             old_artist = old_track['artist']
#             replace_with_choice = int(input(f'Which track would you like to replace {old_name} by {old_artist}? '))
#         except ValueError:
#             print('Please enter the number of the track you wish to choose.')
#     replace_with_index = int(replace_with_choice) - 1
    
#     # build new track object
#     new_track = {}
#     new_track['type'] = track_type
#     if track_level:
#         new_track['level'] = track_level
#     new_track['name'] = track_list[replace_with_index]['name']
#     new_track['artist'] = track_list[replace_with_index]['artist']

#     # check for duplicates
#     # TODO: check for duplicates excluding track being replaced
#     # TODO: check for choosing same song as replacing
#     if new_track in setlist:
#         keep_duplicate_choice = None
#         while keep_duplicate_choice not in ['y', 'n', 'Y', 'N']:
#             new_name = new_track['name']
#             new_artist = new_track['artist']
#             keep_duplicate_choice = input(f'The track {new_name} by {new_artist} is already included elsewhere in your setlist. Would you like to keep it [y/n]? ')
#         if keep_duplicate_choice == 'y':
#             setlist[track_index] = new_track
#         else:
#             retry_choice = None
#             while retry_choice not in ['cancel', 'new']:
#                 retry_choice = input('Enter \'new\' to choose another track or \'cancel\' to keep your current setlist: ')
#             if retry_choice == 'new':
#                 replace_track_user_choice(track_num, setlist)
#     else:
#         setlist[track_index] = new_track



# # currently unused because user input is chosen from a list, so validation not required
    # def validate_user_input(self, difficulty, length, version):
    #     possible_difficulties = ['beginner', 'advanced']
    #     possible_lengths = ['15', '30', '45']
    #     possible_versions = ['a', 'b']

    #     if not difficulty or str(difficulty).lower() not in possible_difficulties:
    #         return False
    #     if not length or length not in possible_lengths:
    #         return False
    #     if not version or str(version).lower() not in possible_versions:
    #         return False
    #     return True