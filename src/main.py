from setlist_builder import SetlistBuilder

def main():
    user_input = get_setlist_requirements()
    setlist_builder = SetlistBuilder(user_input[0], user_input[1], user_input[2])
    setlist = setlist_builder.build_setlist()
    setlist_builder.print_setlist()

    accepted = False
    while not accepted:
        accepted_input = None
        while accepted_input not in ['y', 'n', 'Y', 'N']:
            accepted_input = input('Accept [y/n]? ').lower()
        if accepted_input == 'y':
            accepted = True
        else:
            change_track_num = get_track_change_input(setlist)
            if change_track_num == 'cancel':
                accepted = True
            else:
                replace_method_choice = None
                while replace_method_choice not in ['1','2']:
                    replace_method_choice = input('Would you like to replace with a random song or manually choose a song?\n[1] Random\n[2] Manual\n')
                if replace_method_choice == '1':
                    setlist = setlist_builder.replace_track(int(change_track_num))
                    setlist_builder.print_setlist()
                # else:
        #             replace_track_user_choice(int(change_track_num), setlist)
                    # setlist_builder.print_setlist()
    setlist_builder.print_setlist()


def get_setlist_requirements():
    difficulty_choice = None
    while difficulty_choice not in ['1','2']:
        print('Enter the corresponding number to choose.')
        difficulty_choice = input('Choose your difficulty:\n[1] Beginner\n[2] Advanced\n')
    if difficulty_choice == '1':
        difficulty = 'beginner'
    else:
        difficulty = 'advanced'

    length_choice = None
    while length_choice not in ['1','2','3']:
        length_choice = input('Choose your class length:\n[1] 15 min\n[2] 30 min\n[3] 45 min\n')
    if length_choice == '1':
        length = '15'
    elif length_choice == '2':
        length = '30'
    else:
        length = '45'
    
    version_choice = None
    while version_choice not in ['1','2']:
        version_choice = input('Choose your setlist version:\n[1] A\n[2] B\n')
    if version_choice == '1':
        version = 'a'
    else:
        version = 'b'
    return (difficulty, length, version)

def get_track_change_input(setlist):
    change_track_num = None
    while change_track_num not in range(1, len(setlist)+1) and change_track_num != 'cancel':
        change_track_num = input('Enter the number of the track you want to change or \'cancel\' to cancel: ')
        if change_track_num == 'cancel':
            return 'cancel'
        try:
            change_track_num = int(change_track_num)
        except ValueError:
            print('Please enter the number of the track you wish to replace.')
    return change_track_num

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

# def print_setlist(setlist):
#     for index, track in enumerate(setlist):
#         track_type = str(track['type']).capitalize()
#         track_name = track['name']
#         track_artist = track['artist']
#         if 'level' in track:
#             track_level = track['level']
#             print(f'{index+1}. {track_type} Level {track_level} - {track_name} by {track_artist}')
#         else:
#             print(f'{index+1}. {track_type} - {track_name} by {track_artist}')

if __name__ == "__main__":
    main()