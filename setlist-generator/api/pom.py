import json
import random
from exceptions import TrackNotFoundError, DuplicateIDError

POM_TEMPLATE_LOCATION = '../json/pom_setlist_template.json'
POM_TRACK_LIST_LOCATION = '../json/pom_track_list.json'

def build_pom_setlist(length):
    """ Creates setlist for current template and vars """
    template = _parse_pom_setlist_template(length)
    print(template)

    setlist = []
    for slot in template:
        setlist_track = _build_new_track(setlist, slot)
        setlist.append(setlist_track)
    return setlist

def _parse_pom_setlist_template(length):
    """ Transform setlist from JSON file text to JSON object as global var """

    with open(POM_TEMPLATE_LOCATION, 'r', encoding='UTF-8') as template_file:
        data = template_file.read()
    template_file.close()
    data_json = json.loads(data)
    template = data_json[length]
    return template
    
def _build_new_track(setlist, track_template):
    """ Chooses and builds a single setlist track after filtering for dupes and requirements"""
    track_type = track_template['type']
    track_options = _parse_pom_track_list(track_type)

    ids_in_setlist = list(map(lambda track: track['id'], setlist))
    track_options = list(filter(lambda track: track['id'] not in ids_in_setlist, track_options))

    if len(track_options) == 0:
        raise TrackNotFoundError(f'No tracks available of type {track_type} for slot {track_template}."')

    chosen_track = track_options[random.randrange(0, len(track_options))]
    
    new_track = {}
    new_track['type'] = track_type
    new_track['name'] = chosen_track['name']
    new_track['artist'] = chosen_track['artist']
    new_track['id'] = chosen_track['id']

    return new_track

def _parse_pom_track_list(track_type):
    """ Transforms known tracks from JSON file text to JSON object """
    with open(POM_TRACK_LIST_LOCATION, 'r', encoding='UTF-8') as pom_track_list_file:
        data = pom_track_list_file.read()
    pom_track_list_file.close()
    data_json = json.loads(data)
    try:
        pom_track_list = data_json[str(track_type)]
    except KeyError as exc:
        raise TrackNotFoundError(f'No track of type {track_type} available in list of known songs. Please choose a different setlist or update the song list.') from exc
    return pom_track_list

def get_pom_replacement_track_options(setlist, track_num):
    """ Gets list of tracks with same params as given track_num """
    # get old track details
    track_index = int(track_num) - 1
    old_track = setlist[track_index]
    track_type = old_track['type']

    # get user choice
    track_options = _parse_pom_track_list(track_type)

    # filter duplicates
    ids_in_setlist = list(map(lambda track: track['id'], setlist))
    track_options = list(filter(lambda track: track['id'] not in ids_in_setlist, track_options))

    return track_options

def replace_pom_track(setlist, replace_track_num, new_track_id):
    """ Replaces given track with given new track in setlist """

    # get new track based on id
    new_track = _find_track_by_id(new_track_id)

    track_index = int(replace_track_num) - 1
    old_track = setlist[track_index]
    track_type = old_track['type']

    insert = {}
    insert['type'] = track_type
    insert['name'] = new_track['name']
    insert['artist'] = new_track['artist']
    insert['id'] = new_track['id']

    setlist[track_index] = insert
    return setlist

def _find_track_by_id(track_id):
    """ Transforms track with given id from JSON file text to JSON object """
    with open(POM_TRACK_LIST_LOCATION, 'r', encoding='UTF-8') as pom_track_list_file:
        data = pom_track_list_file.read()
    pom_track_list_file.close()

    data_json = json.loads(data)
    track = []
    for type_entry in data_json:
        # curr_data = data_json[type_entry]
        track = list(filter(lambda t: t['id'] == int(track_id), data_json[type_entry]))
        if len(track) > 1:
            raise DuplicateIDError('There is more than one track with the ID ' + track_id + ' found in the POUND track list.')
        if len(track) == 1:
            return track[0]
    if len(track) == 0:
        raise TrackNotFoundError('There is no track with ID ' + track_id + ' found in the POUND track list.')
    return track[0]