from pom_setlist_builder import PomSetlistBuilder

def main_pom():
    """ runner for PomSquad workflow """
    setlist_params = get_setlist_params()
    pom_setlist_builder = PomSetlistBuilder(setlist_params[0], setlist_params[1], setlist_params[2])
    setlist = pom_setlist_builder.build_setlist()
    print_setlist(setlist)
    
    while not prompt_setlist_accepted():
        change_track_num = get_track_change_input(setlist)
        if change_track_num:
            handle_track_replacement(pom_setlist_builder, change_track_num, setlist)
    
def get_setlist_params():
    """ Ask user for setlist parameters """
    params = [
            {'name':'length', 'options':['20', '30', '50']},
            {'name':'template file name'},
            {'name':'songlist file name'}
        ]
    
    choices = []
    for param in params:
        choice_index = None
        choice = None
        if 'options' in param:
            prompt = 'Please choose the ' + param['name'] + ':\n'
            for index, option in enumerate(param['options']):
                prompt += f'[{index+1}] {option}\n'
            while choice_index not in range(1, len(param['options']) + 1):
                choice_index = int(input(prompt))
                choice = param['options'][choice_index-1]
        else: 
            prompt = 'Please enter the ' + param['name'] + ':\n'
            choice = input(prompt)
        choices.append(choice)
    return choices

def print_setlist(setlist):
    """ Print setlist in numbered order """
    for index, track in enumerate(setlist):
        track_type = str(track['type']).capitalize()
        track_name = track['name']
        track_artist = track['artist']
        print(f'{index+1}. {track_type} - {track_name} by {track_artist}')

def prompt_setlist_accepted():
    """ get user input to determine if setlist is accepted """
    accepted_input = None
    while accepted_input not in ['y', 'n']: 
        accepted_input = input('Accept [y/n]? ').lower()

    if accepted_input == 'y':
        return True
    else:
        return False
    
def get_track_change_input(setlist):
    """ get user input to change a track in the setlist """
    change_track_num = None
    while change_track_num not in range(1, len(setlist)+1):
        selected_track_num = input('Enter the number of the track you want to change or \'cancel\' to cancel: ')
        if selected_track_num == 'cancel':
            return None
        try:
            change_track_num = int(selected_track_num)
        except ValueError:
            print('Please enter a number or \'cancel\'.')
    return change_track_num

def handle_track_replacement(pom_setlist_builder:PomSetlistBuilder, change_track_num, setlist):
    """ orchestrate track replacement - auto or manual """
    selected_replacement_type = prompt_replacement_type()

    if selected_replacement_type == 'random':
        setlist = pom_setlist_builder.auto_replace_track(setlist, change_track_num)
    else: # Manual
        setlist = handle_manual_replacement(pom_setlist_builder, setlist, change_track_num)
    print_setlist(setlist)

def prompt_replacement_type():
    """ get user input ot determine which type of track replacement to use """
    replace_method_choice = None
    while replace_method_choice not in ['1','2']:
        replace_method_choice = input('Would you like to replace with a random song or manually choose a song?\n[1] Random\n[2] Manual\n')
    if replace_method_choice == '1':
        return 'random'
    else:
        return 'manual'
    
def handle_manual_replacement(pom_setlist_builder:PomSetlistBuilder, setlist, change_track_num):
    """ orchestrate manual replacement with user input """
    replacement_options = pom_setlist_builder.get_replacement_track_options(setlist, change_track_num)
    
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

    return pom_setlist_builder.replace_track(setlist, change_track_num, new_track)