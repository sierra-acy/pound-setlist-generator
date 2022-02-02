import json

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

def get_song_list(track_type, level, path_to_songs):
    with open(path_to_songs + 'song_list.json', 'r') as song_list_file:
        data = song_list_file.read()
        data_json = json.loads(data)
        if level:
            song_list = data_json[track_type.lower()][level]
        else:
            song_list = data_json[track_type.lower()]
    return song_list
    
if __name__ == "__main__":
    main()