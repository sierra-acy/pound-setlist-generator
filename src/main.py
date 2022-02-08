
import json
import random

def main():
    user_input = get_user_input()
    setlist = build_setlist(user_input[0], user_input[1], user_input[2])
    print_setlist(setlist)

    accepted = False
    while not accepted:
        accepted_input = None
        while accepted_input not in ['y', 'n', 'Y', 'N']:
            accepted_input = input('Accept (y/n)?').lower()
        if accepted_input == 'y':
            accepted = True
        else:
            change_track_num = None
            while change_track_num not in range(1, len(setlist)+1):
                try:
                    change_track_num = int(input('Enter the number of the track you want to change: '))
                except ValueError:
                    print('Please enter the number of the track you wish to replace.')

            replace_method_choice = None
            while replace_method_choice not in ['1','2']:
                replace_method_choice = input('Would you like to replace with a random song or manually choose a song?\n[1] Random\n[2] Manual\n')
            if replace_method_choice == '1':
                replace_track(int(change_track_num), setlist)
            else:
                replace_track_user_choice(int(change_track_num), setlist)
            print_setlist(setlist)
    

def get_user_input():
    difficulty_choice = None
    difficulty = 'beginner'
    while difficulty_choice not in ['1','2']:
        print('Enter the corresponding number to choose.')
        difficulty_choice = input('Choose your difficulty:\n[1] Beginner\n[2] Advanced\n')
    if difficulty_choice == '2':
        difficulty_choice = 'advanced'

    length_choice = None
    length = '15'
    while length_choice not in ['1','2','3']:
        length_choice = input('Choose your class length:\n[1] 15 min\n[2] 30 min\n[3] 45 min\n')
    if length_choice == '2':
        length = '30'
    elif length_choice == '3':
        length = '45'
    
    version_choice = None
    version = 'a'
    while version_choice not in ['1','2']:
        version_choice = input('Choose your setlist version:\n[1] A\n[2] B\n')
    if version_choice == '2':
        version = 'b'
    return (difficulty, length, version)

def get_setlist_template(difficulty, length, version):
    template = None
    with open('src/setlist_template.json', 'r') as template_file:
        data = template_file.read()
        data_json = json.loads(data)
        template = data_json[difficulty.lower()][length][version.lower()]

    template_file.close()
    return template

def get_track_list(track_type, level):
    track_list = None
    with open('src/track_list.json', 'r') as track_list_file:
        data = track_list_file.read()
        data_json = json.loads(data)
        try:
            track_list = data_json[track_type.lower()]
        except KeyError:
            track_list_file.close()
            raise Exception(f'No track of type {track_type} available in list of known songs. Please choose a different setlist or update the song list.')

        if level:
            try:
                track_list = track_list[level]
            except KeyError:
                track_list_file.close()
                raise Exception(f'No track of type {track_type} with level {level} available in list of known songs. Please choose a different setlist or update the song list.')

    track_list_file.close()
    return track_list

def build_setlist(difficulty, length, version):
    setlist = []
    template = get_setlist_template(difficulty, length, version)

    # build setlist
    for slot in template:
        track_type = slot['type']
        track_level = None
        if track_type != 'cooldown' and track_type != 'warmup':
            track_level = slot['level']
        
        track_list = get_track_list(track_type, track_level)
        duplicate_track = True
        # choose random track and ensure no duplicates
        while duplicate_track:
            track_index = random.randrange(0, len(track_list))
            chosen_track = track_list[track_index]

            setlist_track = {}
            setlist_track['type'] = track_type
            if track_level is not None:
                setlist_track['level'] = track_level
            setlist_track['name'] = chosen_track['name']
            setlist_track['artist'] = chosen_track['artist']
            if(setlist_track not in setlist):
                duplicate_track = False

        setlist.append(setlist_track)
    return setlist

# currently unused because user input is chosen from a list, so validation not required
def validate_user_input(difficulty, length, version):
    possible_difficulties = ['beginner', 'advanced']
    possible_lengths = ['15', '30', '45']
    possible_versions = ['a', 'b']

    if not difficulty or difficulty.lower() not in possible_difficulties:
        return False
    if not length or length not in possible_lengths:
        return False
    if not version or version.lower() not in possible_versions:
        return False
    return True

def replace_track(track_num, setlist):
    track_index = track_num - 1
    old_track = setlist[track_index]
    track_type = old_track['type']
    track_level = None
    if 'level' in old_track:
        track_level = old_track['level']

    duplicate = True
    new_track = {}
    while duplicate:
        track_list = get_track_list(track_type, track_level)
        chosen_track_index = random.randrange(0, len(track_list))
        chosen_track = track_list[chosen_track_index]

        new_track['type'] = track_type
        if track_level:
            new_track['level'] = track_level
        new_track['name'] = chosen_track['name']
        new_track['artist'] = chosen_track['artist']

        if new_track != old_track and new_track not in setlist:
            duplicate = False
    setlist[track_index] = new_track

def replace_track_user_choice(track_num, setlist):
    # get old track details
    track_index = track_num - 1
    old_track = setlist[track_index]
    track_type = old_track['type']

    if 'level' in old_track:
        track_level = old_track['level']
    else:
        track_level = None

    # get user choice  
    track_list = get_track_list(track_type, track_level)  
    if track_level:
        options = f'{str(track_type).capitalize()} level {track_level} tracks:\n'
    else:
        options = f'{str(track_type).capitalize()} tracks:\n'

    for index, track in enumerate(track_list):
        name = track['name']
        artist = track['artist']
        options += f'{index+1}. {name} by {artist}\n'
    print(options)
    replace_with_choice = None
    while replace_with_choice not in range(1, len(track_list)+1):
        try:
            old_name = old_track['name']
            old_artist = old_track['artist']
            replace_with_choice = int(input(f'Which track would you like to replace {old_name} by {old_artist}? '))
        except ValueError:
            print('Please enter the number of the track you wish to choose.')
    replace_with_index = int(replace_with_choice) - 1
    
    # build new track object
    new_track = {}
    new_track['type'] = track_type
    if track_level:
        new_track['level'] = track_level
    new_track['name'] = track_list[replace_with_index]['name']
    new_track['artist'] = track_list[replace_with_index]['artist']

    # check for duplicates
    # TODO: check for duplicates excluding track being replaced
    # TODO: check for choosing same song as replacing
    if new_track in setlist:
        keep_duplicate_choice = None
        while keep_duplicate_choice not in ['y', 'n', 'Y', 'N']:
            new_name = new_track['name']
            new_artist = new_track['artist']
            keep_duplicate_choice = input(f'The track {new_name} by {new_artist} is already included elsewhere in your setlist. Would you like to keep it [y/n]? ')
        if keep_duplicate_choice == 'y':
            setlist[track_index] = new_track
        else:
            retry_choice = None
            while retry_choice not in ['cancel', 'new']:
                retry_choice = input('Enter \'new\' to choose another track or \'cancel\' to keep your current setlist: ')
            if retry_choice == 'new':
                replace_track_user_choice(track_num, setlist)
    else:
        setlist[track_index] = new_track

def print_setlist(setlist):
    for index, track in enumerate(setlist):
        track_type = str(track['type']).capitalize()
        track_name = track['name']
        track_artist = track['artist']
        if 'level' in track:
            track_level = track['level']
            print(f'{index+1}. {track_type} Level {track_level} - {track_name} by {track_artist}')
        else:
            print(f'{index+1}. {track_type} - {track_name} by {track_artist}')

if __name__ == "__main__":
    main()