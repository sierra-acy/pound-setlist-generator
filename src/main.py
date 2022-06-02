import argparse
from setlist_builder import SetlistBuilder

def main():
    """ main runner """

    args = get_args()
    setlist_builder = SetlistBuilder(args['diff'], args['len'], args['version'], args['arm'], args['template'], args['songs'])
    setlist = setlist_builder.build_setlist()
    print_setlist(setlist)

    while not prompt_setlist_accepted():
        change_track_num = get_track_change_input(setlist)
        if change_track_num:
            handle_track_replacement(setlist_builder, change_track_num, setlist)

def get_args():
    """ Setup argument parser """
    parser = argparse.ArgumentParser()
    parser.add_argument('-diff', '-d', required=True, help='difficulty level', choices=['beginner', 'advanced'])
    parser.add_argument('-len', '-l', required=True, help='length of the setlist', choices=['15', '30', '45'])
    parser.add_argument('-version', '-v', required=True, help="version A or B of the setlist", choices=['a', 'b'])
    parser.add_argument('-arm', '-a', default='true', help="true means an arm track will be included, false means one may or may not be incldued", choices=['true', 'false'])
    parser.add_argument('-template', '-t', default='src/setlist_template.json', help='location of template file to use')
    parser.add_argument('-songs', '-s', default='src/track_list.json', help='location of the list of known songs')
    return vars(parser.parse_args())

def get_accepted_input():
    """ get user input to determine if setlist is accepted """
    accepted_input = None
    while accepted_input not in ['y', 'n', 'Y', 'N']:
        accepted_input = input('Accept [y/n]? ').lower()
    return accepted_input.lower()

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

def handle_track_replacement(setlist_builder:SetlistBuilder, change_track_num):
    """ orchestrate track replacement - auto or manual """
    selected_replacement_type = prompt_replacement_type()

    if selected_replacement_type == 'random':
        setlist = setlist_builder.auto_replace_track(setlist, change_track_num)
    else: # Manual
        setlist = handle_manual_replacement(setlist_builder, setlist, change_track_num)
    print_setlist(setlist)

def handle_manual_replacement(setlist_builder:SetlistBuilder, setlist, change_track_num):
    """ orchestrate manual replacement with user input """
    replacement_options = setlist_builder.get_replacement_track_options(setlist, change_track_num)
    
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

    return setlist_builder.replace_track(setlist, change_track_num, new_track)

def prompt_replacement_type():
    """ get user input ot determine which type of track replacement to use """
    replace_method_choice = None
    while replace_method_choice not in ['1','2']:
        replace_method_choice = input('Would you like to replace with a random song or manually choose a song?\n[1] Random\n[2] Manual\n')
    if replace_method_choice == '1':
        return 'random'
    else:
        return 'manual'

def prompt_setlist_accepted():
    """ get user input to determine if setlist is accepted """
    accepted_input = None
    while accepted_input not in ['y', 'n']: 
        accepted_input = input('Accept [y/n]? ').lower()

    if accepted_input == 'y':
        return True
    else:
        return False

def print_setlist(setlist):
    """ Print setlist in numbered order """
    for index, track in enumerate(setlist):
        track_type = str(track['type']).capitalize()
        track_name = track['name']
        track_artist = track['artist']
        track_level = track['level']
        if track_type != 'Warmup' and track_type != 'Cooldown':
            print(f'{index+1}. {track_type} Level {track_level} - {track_name} by {track_artist}')
        else:
            print(f'{index+1}. {track_type} - {track_name} by {track_artist}')

if __name__ == "__main__":
    main()