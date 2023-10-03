from flask import Flask, request

app = Flask(__name__)

@app.route('/pound-setlist', methods=['GET','PUT'])
def generate_pound_setlist():
    """ Generate or Update POUND setlsit """
    if(request.method == 'GET'):
        DUMMY_SETLIST_DATA_POUND = [
            {"id":1, "type":"warmup", "name":"songname1", "artist":"artist1"},
            {"id":2, "type":"set", "level":"1", "name":"songname2", "artist":"artist2"}
        ]
        return DUMMY_SETLIST_DATA_POUND
    elif(request.method == 'PUT'):
        DUMMY_REPLACED_SETLIST_DATA_POUND = [
            {"id":5, "name":"DummySong1", "artist":"DummyArtist1","type":"DummyType1", "level":"DummyLevel1"},
            {"id":2, "type":"set", "level":"1", "name":"songname2", "artist":"artist2"}
        ]
        return DUMMY_REPLACED_SETLIST_DATA_POUND

@app.route('/pom-setlist', methods=['GET','PUT'])
def generate_pom_setlist():
    """ Generate PomSquad Setlist """
    if(request.method == 'GET'):
        DUMMY_SETLIST_DATA_POM = [
        {"id":3, "type":"prancing", "name":"songname1", "artist":"artist1"},
        {"id":4, "name":"songname2", "artist":"artist2"}
        ]
        return DUMMY_SETLIST_DATA_POM
    elif(request.method == 'PUT'):
        DUMMY_REPLACED_SETLIST_DATA_POUND = [
            {"id":5, "name":"DummySong1", "artist":"DummyArtist1","type":"DummyType1", "level":"DummyLevel1"},
            {"id":2, "type":"set", "level":"1", "name":"songname2", "artist":"artist2"}
        ]
        return DUMMY_REPLACED_SETLIST_DATA_POUND
    

@app.route('/pound-replacement-options')
def find_pound_replacement_options():
    """ Find list of matching replacements """
    DUMMYREPLACEMENTOPTIONS= [
        {"id":5, "name":"DummySong1", "artist":"DummyArtist1","type":"DummyType1", "level":"DummyLevel1"},
        {"id":6, "name":"DummySong2", "artist":"DummyArtist2","type":"DummyType1", "level":"DummyLevel1"}
    ]
    return DUMMYREPLACEMENTOPTIONS

@app.route('/pom-replacement-options')
def find_pom_replacement_options():
    """ Find list of matching replacements """
    DUMMYREPLACEMENTOPTIONS= [
        {"id":5, "name":"DummySong1", "artist":"DummyArtist1","type":"DummyType1", "level":"DummyLevel1"},
        {"id":6, "name":"DummySong2", "artist":"DummyArtist2","type":"DummyType1", "level":"DummyLevel1"}
    ]
    return DUMMYREPLACEMENTOPTIONS