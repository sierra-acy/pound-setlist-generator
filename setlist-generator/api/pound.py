import json
import random
from exceptions import TrackAvailabilityError

POUND_TEMPLATE_LOCATION = '../json/pound_setlist_template.json'
POUND_TRACK_LIST_LOCATION = '../json/pound_track_list.json'

def build_pound_setlist(difficulty, length, version, include_arm_track):
    """ Creates setlist for current template and vars """
    template = _parse_pound_setlist_template(difficulty, length, version)
    setlist = []
    for slot in template:
        setlist_track = _build_new_track(setlist, slot, include_arm_track)
        setlist.append(setlist_track)
    return setlist

def _parse_pound_setlist_template(difficulty, length, version):
    """ Transform setlist from JSON file text to JSON object as global var """
    with open(POUND_TEMPLATE_LOCATION, 'r', encoding='UTF-8') as template_file:
        data = template_file.read()
    template_file.close()
    data_json = json.loads(data)
    template = data_json[difficulty][length][version]
    return template

def _build_new_track(setlist, track_template, include_arm_track):
    """ Chooses and builds a single setlist track, after filtering for dupes and requirements"""
    track_type = track_template['type']
    track_level = None
    if 'level' in track_template:
        track_level = track_template['level']
    track_options = _parse_pound_track_list(track_type, track_level)

    is_arm_track = False
    if 'canBeArmTrack' in track_template and include_arm_track:
        track_options = list(filter(lambda track: track['canBeArmTrack'] is True, track_options))
        is_arm_track = True

    track_options = _filter_duplicates(setlist, track_options)
    
    if len(track_options) == 0:
        raise TrackAvailabilityError(f'No track available of type {track_type} with level {track_level} for slot {track_template}."')

    chosen_track = track_options[random.randrange(0, len(track_options))]

    new_track = {}
    new_track['type'] = track_type
    new_track['level'] = track_level
    new_track['name'] = chosen_track['name']
    new_track['artist'] = chosen_track['artist']
    new_track['isArmTrack'] = is_arm_track
    new_track['id'] = chosen_track['id']

    return new_track

def _parse_pound_track_list(track_type, track_level):
    """ Transforms known tracks from JSON file text to JSON object """
    with open(POUND_TRACK_LIST_LOCATION, 'r', encoding='UTF-8') as pound_track_list_file:
        data = pound_track_list_file.read()
    pound_track_list_file.close()

    data_json = json.loads(data)
    try:
        pound_track_list = data_json[str(track_type)]
    except KeyError as exc:
        raise TrackAvailabilityError(f'No track of type {track_type} available in list of known songs. Please choose a different setlist or update the song list.') from exc

    if track_level:
        try:
            pound_track_list = pound_track_list[str(track_level)]
        except KeyError as exc:
            raise TrackAvailabilityError(f'No track of type {track_type} with level {track_level} available in list of known songs. Please choose a different setlist or update the song list.') from exc
    return pound_track_list

def get_pound_replacement_track_options(setlist, track_num, include_arm_track, difficulty, length, version):
    """ Gets list of tracks with same params as given track_num """

    # get old track details
    track_index = int(track_num) - 1
    old_track = setlist[track_index]
    track_type = old_track['type']
    track_level = old_track['level']

    # get user choice
    track_options = _parse_pound_track_list(track_type, track_level)
    template = _parse_pound_setlist_template(difficulty, length, version)
    if 'canBeArmTrack' in template[track_index] and include_arm_track:
        track_options = list(filter(lambda track: track['canBeArmTrack'] is True, track_options))

    # filter duplicates
    track_options = _filter_duplicates(setlist, track_options)

    return track_options

def _filter_duplicates(setlist, options):
    """ Filters duplicate songs out of list based on id """
    ids_in_setlist = list(map(lambda track: track['id'], setlist))
    return list(filter(lambda track: track['id'] not in ids_in_setlist, options))