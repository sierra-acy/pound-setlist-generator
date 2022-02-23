from setlist_builder import SetlistBuilder

def main():
    """ main runner """
    user_input = get_setlist_requirements()
    setlist_builder = SetlistBuilder(user_input[0], user_input[1], user_input[2])
    setlist = setlist_builder.build_setlist()
    setlist_builder.print_setlist()
    while get_accepted_input() == 'n':
        change_track_num = get_track_change_input(setlist)
        if change_track_num != 'cancel':
            handle_track_replacement(setlist_builder, change_track_num, setlist)
            setlist_builder.print_setlist()

def get_setlist_requirements():
    """ get user input for setlist params """
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
    """ get user input to change a track in the setlist """
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

def handle_track_replacement(setlist_builder:SetlistBuilder, change_track_num, setlist):
    """ orchestrate track replacement - auto or manual """
    replace_method_choice = None
    while replace_method_choice not in ['1','2']:
        replace_method_choice = input('Would you like to replace with a random song or manually choose a song?\n[1] Random\n[2] Manual\n')

    if replace_method_choice == '1': # Random
        setlist_builder.auto_replace_track(int(change_track_num))
        # setlist_builder.print_setlist()
    else: # Manual
        handle_manual_replacement(setlist_builder, change_track_num)

def handle_manual_replacement(setlist_builder:SetlistBuilder, change_track_num):
    """ orchestrate manual replacement with user input """
    replacement_options = setlist_builder.get_replacement_track_options(int(change_track_num))
    setlist = setlist_builder.get_setlist()
    
    # prepare prompt
    old_name = setlist[change_track_num-1]['name']
    old_artist = setlist[change_track_num-1]['artist']
    prompt = f'Which track would you like to replace {old_name} by {old_artist}?\n'
    for index, option in enumerate(replacement_options):
        option_name = option['name']
        option_artist = option['artist']
        prompt += f'[{index+1}] {option_name} by {option_artist}\n'

    # get input
    replace_with_choice = None
    while replace_with_choice not in range(1, len(replacement_options)+1):
        try:
            replace_with_choice = int(input(prompt))
        except ValueError:
            print('Please enter the number of the track you wish to choose.')

    new_track = replacement_options[replace_with_choice-1]

    # check for duplicates
    if setlist_builder.new_track_is_duplicate(new_track, change_track_num):
        keep_duplicate_choice = None
        while keep_duplicate_choice not in ['y', 'n', 'Y', 'N']:
            new_name = new_track['name']
            new_artist = new_track['artist']
            keep_duplicate_choice = input(f'The track {new_name} by {new_artist} is already included elsewhere in your setlist. Would you like to include it anyway [y/n]? ')
        
        if keep_duplicate_choice.lower() == 'y':
            setlist = setlist_builder.replace_track(change_track_num, new_track)
        else:
            retry_choice = None
            while retry_choice not in ['cancel', 'new']:
                retry_choice = input('Enter \'new\' to choose another track or \'cancel\' to keep your current setlist: ')
            
            if retry_choice == 'new':
                handle_manual_replacement(setlist_builder, change_track_num)
    else:
        setlist_builder.replace_track(change_track_num, new_track)

def get_accepted_input():
    """ get user input to determine if setlist is accepted """
    accepted_input = None
    while accepted_input not in ['y', 'n', 'Y', 'N']:
        accepted_input = input('Accept [y/n]? ').lower()
    return accepted_input.lower()

if __name__ == "__main__":
    main()