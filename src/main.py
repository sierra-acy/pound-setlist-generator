from xml.etree.ElementInclude import include
from setlist_builder import SetlistBuilder

def main():
    # SCOTT: in general, I find this main function pretty good. very easy to read, mostly clear what everything is doing.
    # P-dang good. 
    #
    # Aside from all the mostly unimportant nits below, I think my only major point of feedback is that reading through
    # main, it's not clear where the line is drawn between a setlist and a setlist_builder. Why do you use the 
    # setlist_builder for printing a setlist and not the setlist itself? what's the advantage of splitting them apart?

    """ main runner """
    # SCOTT nit: the function is called get_setlist_requirements() but the variable it's assigned to is called
    # user_input. IMO the `user_input` variable should be called something like setlist_requirements or setlist_params
    # 
    # SCOTT nit: IMO 'getters' should be basically instanteous, non-blocking, non-mutating reads. To better communicate
    # what happens in this function consider `prompt_user_for_setlist_requirements()` even though its a bit wordier.
    # This feedback applies to a number of getters which prompt for user input. Though again this is a nit and I don't
    # feel super strongly about this if you prefer the `get` lingo.
    user_input = get_setlist_requirements()

    # SCOTT nit: just looking at this SetlistBuilder constructor it's not clear what each of these array values are.
    # Consider using a stronger type so you could pass `user_input.foo` instead of `user_input[1]` and its clearer what
    # constructs the setlist builder
    setlist_builder = SetlistBuilder(user_input[0], user_input[1], user_input[2], user_input[3])

    # SCOTT nit: why build the setlist here? you don't use it unless it's not accepted. Consider delaying building it
    # until you need it inside the while loop
    setlist = setlist_builder.build_setlist()
    setlist_builder.print_setlist()
    # SCOTT nit: personal preference, I think using random string literals reads less clearer than enums or constants.
    # Maybe even a bool. Though the more I think about this the less strongly I feel and honestly the string literal
    # really isn't that bad but throwing out my gut reaction.
    # e.g. `while get_accepted_input() == False:` or `while not prompt_setlist_accepted():` or something
    while get_accepted_input() == 'n':
        # SCOTT: I find it slightly tricky that get_track_change_input can return two different types of values.
        # valid values are numbers but a cancellation is a string
        # what about returning "None" to mean cancel?
        change_track_num = get_track_change_input(setlist)
        if change_track_num != 'cancel':
            # SCOTT: it doesn't look like the `setlist` parameter is used. just the setlist_builder. 
            # also passing  both wouldn't make sense because the setlist_builder can always be used to generate the
            # associated setlist methinks.
            # SCOTT: you mentioned wanting to separate user input from behavior. This seems like a good place to do that
            #
            # effectively handle_track_replacement just gets split apart
            # ```
            # replacement_type = prompt_user_for_track_replacement_type()
            # if replacement_type == 'random':
            #     auto_replace_track(...)
            # else: `
            #     handle_manual_replacement(...)
            handle_track_replacement(setlist_builder, change_track_num, setlist)
            setlist_builder.print_setlist()

# SCOTT: UX food-for-thought 
# you only ever prompt for these requirements once at the very start of the program
# consider passing these requirements in as command line arguments instead (or maybe just
# allowing that as an option). Definitely not a priority of things to worry about but
# if you find yourself wanting to run this quicker and more often, cmdline params can be useful
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

    # SCOTT nit: I think this is a typo and you meant to write `include_arm_track` here
    # include_arm_track_choice is only needed in the if-branch and currently it looks like `include_arm_track` is 
    # localized within the if-else scope so I'm not sure if the value you're returning below will ever actually be
    # True or False (it may always be None)
    include_arm_track_choice = None
    if length == '30' or length == '45':
        # scott nit: elsewhere for your accept prompt you did 'y'/'n' rather than the full 'yes'/'no'
        # might be nice to standardize on one.
        while include_arm_track_choice not in ['yes', 'no', 'Yes', 'No']:
            include_arm_track_choice = input('Do you want to include an arm track? [yes/no] \n')
        # scott nit: coult be a oneliner `include_arm_track = include_arm_track_choice.lower() == 'yes'`
        if include_arm_track_choice.lower() == 'yes':
            include_arm_track = True
        else:
            include_arm_track = False
    else:
        include_arm_track = False

    return (difficulty, length, version, include_arm_track)

def get_track_change_input(setlist):
    """ get user input to change a track in the setlist """
    change_track_num = None
    # SCOTT nit: I don't think you need to check for `!= 'cancel'` here. The only path where we get a 'cancel' input early
    # returns before hitting this while loop again
    while change_track_num not in range(1, len(setlist)+1) and change_track_num != 'cancel':
        change_track_num = input('Enter the number of the track you want to change or \'cancel\' to cancel: ')
        if change_track_num == 'cancel':
            return 'cancel'
        try:
            # SCOTT nit: it slightly gives me the heebie jeebies that `change_track_num` takes on multiple types 
            # throughout this function. First its a string then we make it an int here. I suppose it's not a totally
            # foreign pattern in python but I consider it a potential point of confusion.
            change_track_num = int(change_track_num)
        except ValueError:
            # SCOTT nit: if you enter in a non-cancel value and we hit this except path, won't it double print this
            # message basically? like it will print htis here and then at the start of the loop it'll ask you again
            print('Please enter the number of the track you wish to replace.')
    return change_track_num

def handle_track_replacement(setlist_builder:SetlistBuilder, change_track_num, setlist):
    """ orchestrate track replacement - auto or manual """
    replace_method_choice = None
    while replace_method_choice not in ['1','2']:
        replace_method_choice = input('Would you like to replace with a random song or manually choose a song?\n[1] Random\n[2] Manual\n')

    if replace_method_choice == '1': # Random
        # SCOTT nit: isn't change_track_num already passed in as an int?
        setlist_builder.auto_replace_track(int(change_track_num))
        # setlist_builder.print_setlist()
    else: # Manual
        handle_manual_replacement(setlist_builder, change_track_num)

# SCOTT: previously you mentioned a desire to split apart the user input prompts from the main logic
# I'm not sure if one of the ones you were referring to was this function but just in case I'll call out that while
# there's a lot of mixing going on in this function, I don't think you haven't already achieved your splitting goals.
# the main logic already is in its own functions and its just that the meat of this function is prompting for user-input
# 
# maybe if you were really antsy about it you could clean that up by splitting out some helper functions to make
# all the user prompts less dominating of the function body
def handle_manual_replacement(setlist_builder:SetlistBuilder, change_track_num):
    """ orchestrate manual replacement with user input """
    # SCOTT nit: isn't change_track_num already an int?
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
            # SCOTT NIT: is this assignment used anywhere?
            setlist = setlist_builder.replace_track(change_track_num, new_track)
        else:
            retry_choice = None
            while retry_choice not in ['cancel', 'new']:
                retry_choice = input('Enter \'new\' to choose another track or \'cancel\' to keep your current setlist: ')
            
            if retry_choice == 'new':
                # SCOTT NIT: my eyebrows are slightly raised at this recursion but it's mostly a reflexive gut thing.
                # Wouldn't bother fixing what ain't broke but I tend to get a little meh around recursion.
                handle_manual_replacement(setlist_builder, change_track_num)
    else:
        setlist_builder.replace_track(change_track_num, new_track)

def get_accepted_input():
    # SCOTT nit: is this function specific to accepting the setlist? if-so should it be in charge of printing the setlist
    # so that the calling while loop doesn't have to print the setlist in two places?
    """ get user input to determine if setlist is accepted """
    accepted_input = None
    # SCOTT nit: you call lower on the accepted_input. do you need to check for upper and lower case?
    while accepted_input not in ['y', 'n', 'Y', 'N']: 
        accepted_input = input('Accept [y/n]? ').lower()
    # SCOTT nit: do you need to call .lower() again? the accepted input should always be in lower case since you only
    # capture it in lower case
    return accepted_input.lower()

if __name__ == "__main__":
    main()

# SCOTT: random food for thought
# 
# I see a lot of similar user-prompting patterns
# I wouldn't prioritize this but it gives me the idea that there's an opportunity to maybe cleanup some of this code
# by defining some shared user prompt helpers.