
import json
import random

def main():
    user_input = get_user_input()
    setlist = build_setlist(user_input[0], user_input[1], user_input[2])
    print_setlist(setlist)

    accepted = False
    while not accepted:
        accepted_input = input('Accept (y/n)?').lower()
        if accepted_input == 'y':
            accepted = True
        else:
            change_track_num = input('Enter the number of the track you want to change: ')
            replace_track(int(change_track_num), setlist)
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
            raise Exception('No track of type {} available in list of known songs. Please choose a different setlist or update the song list.'.format(track_type))

        if level:
            try:
                track_list = track_list[level]
            except KeyError:
                track_list_file.close()
                raise Exception('No track of type {} with level {} available in list of known songs. Please choose a different setlist or update the song list.'.format(track_type, level))

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


def print_setlist(setlist):
    for index, track in enumerate(setlist):
        if 'level' in track:
            print('{}. {} Level {} - {} by {}'.format(index+1, str(track['type']).capitalize(), track['level'], track['name'], track['artist']))
        else:
            print('{}. {} - {} by {}'.format(index+1, str(track['type']).capitalize(), track['name'], track['artist']))

if __name__ == "__main__":
    main()