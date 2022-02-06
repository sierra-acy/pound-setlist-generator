import json
import random

def main():
    template = get_setlist_template("beginner", "15", "a")

def get_setlist_template(difficulty, length, version, path_to_template):
    template = None
    with open(path_to_template + 'setlist_template.json', 'r') as template_file:
        data = template_file.read()
        data_json = json.loads(data)
        template = data_json[difficulty.lower()][length][version.lower()]
    template_file.close()
    return template

def get_track_list(track_type, level, path_to_tracks):
    with open(path_to_tracks + 'track_list.json', 'r') as track_list_file:
        data = track_list_file.read()
        data_json = json.loads(data)
        track_list = None
        try:
            track_list = data_json[track_type.lower()]
        except KeyError:
            print('No type \"{}\" found in track list.'.format(track_type))

        if level:
            try:
                track_list = track_list[level]
            except KeyError:
                print('No level \"{}\" found in track list for type \"{}\"'.format(level, track_type))
    return track_list

def build_setlist(difficulty, length, version, path_to_template, path_to_songs):
    setlist = []
    template = get_setlist_template(difficulty, length, version, path_to_template)

    # build setlist
    for slot in template:
        track_type = slot['type']
        track_level = None
        if track_type != 'cooldown' and track_type != 'warmup':
            track_level = slot['level']
        
        track_list = get_track_list(track_type, track_level, path_to_songs)
        duplicate_track = True
        # choose random track and ensure no duplicates
        while duplicate_track:
            track_index = random.randrange(0, len(track_list))
            chosen_track = track_list[track_index]

            setlist_track = {}
            if type is not None:
                setlist_track['type'] = track_type
            setlist_track['level'] = track_level
            setlist_track['name'] = chosen_track['name']
            setlist_track['artist'] = chosen_track['artist']
            if(setlist_track not in setlist):
                duplicate_track = False

        setlist.append(setlist_track)
    return setlist

# def print_setlist(setlist):
    # TODO

if __name__ == "__main__":
    main()