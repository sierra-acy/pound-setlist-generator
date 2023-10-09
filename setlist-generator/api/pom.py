import json
import random
from exceptions import TrackNotFoundError

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