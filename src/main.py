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

if __name__ == "__main__":
    main()