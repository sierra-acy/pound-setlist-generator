from flask import Flask, request
from pound import build_setlist as build_pound_setlist
from pom import build_setlist as build_pom_setlist

app = Flask(__name__)

@app.route('/pound-setlist', methods=['GET','PUT'])
def pound_setlist():
    """ Generate or Update POUND setlsit """
    if(request.method == 'GET'):
        args = request.args
        return build_pound_setlist(args.get('difficulty'), args.get('length'), args.get('version'), args.get('include_arm_track'))

    if(request.method == 'PUT'):
        DUMMY_REPLACED_SETLIST_DATA_POUND = [
            {"id":5, "name":"DummySong1", "artist":"DummyArtist1","type":"DummyType1", "level":"DummyLevel1"},
            {"id":2, "type":"set", "level":"1", "name":"songname2", "artist":"artist2"}
        ]
        return DUMMY_REPLACED_SETLIST_DATA_POUND

@app.route('/pom-setlist', methods=['GET','PUT'])
def pom_setlist():
    """ Generate PomSquad Setlist """
    if(request.method == 'GET'):
        args = request.args
        return build_pom_setlist(args.get('length'))

    if(request.method == 'PUT'):
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