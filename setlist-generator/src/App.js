import React, { useState } from 'react';
import './App.css';


function RadioOption({ id, name, value, label }) {
  return (
    <div>
      <input type="radio" id={id} name={name} value={value}/>
      <label for={id}>{label}</label><br/>
    </div>
  );
}

function RadioGroup({ radioGroupLabel, optionsList }) {
  const options = []
  
  for(i in optionsList) {
    const id = optionsList[i] + i;
    
    options.push(
      <RadioOption id={id} name={id} value={optionsList[i]} label={optionsList[i]} />
    );
  }

  return (
    <div>
      <p>{radioGroupLabel}:</p><br/>
      {options}
    </div>
  );
}

function CheckboxOption({ checkboxLabel }) {
  return(
    <div>
      <input type="checkbox" id={checkboxLabel} name={checkboxLabel} value={checkboxLabel}/>
      <label for={checkboxLabel}>{checkboxLabel}</label>
    </div>
  );
}

function PoundTrack({ name, artist, type, level }) {
  const withLevel = <p>{type} Level {level}: {name} by {artist}</p>
  const noLevel = <p>{type}: {name} by {artist}</p>
  const trackHtml = level !== null ? withLevel : noLevel;

  return(
    trackHtml
  );
}

function PomTrack({ name, artist, type }) {
  const withType = <p>{type}: {name} by {artist}</p>
  const noType = <p>{name} by {artist}</p>
  const trackHtml = type !== null ? withType : noType;

  return(
    trackHtml
  );
}

function PomSettingsForm({ onClassLengthChange }) {
  const classLengthList = ["20", "30", "50"];

  return(
    <div>
      <form>
        <RadioGroup radioGroupLabel="Class Length" optionsList={classLengthList}/>
        <button type="submit" value="Generate"/>
      </form>
    </div>
  );
}

function PomSetlist({ setlistData, classLength }) {
  let setlist = [];
  setlistData.forEach((trackData) => {
    let type = trackData.contains('type') ? trackData.type : null;
    setlist.push(
      <li><PomTrack name={trackData.name} artist={trackData.artist} type={type}/></li>
    );
  });

  return (
    <div>
      <ol>
        { setlist }
      </ol>
    </div>
  );
}

function PoundSettingsForm( { onDifficultyChange, onClassLengthChange, onSetlistVersionChange, onIncludeArmTrackChange }) {
  const difficultyList = ["Beginner", "Advanced"];
  const classLengthList = ["15 min", "30 min", "45 min"];
  const setlistVersionList = ["A (default)", "B"];

  return(
    <div>
      <form>
        <RadioGroup radioGroupLabel="Class Difficulty" optionList={difficultyList}/><br/>
        <RadioGroup radioGroupLabel="Class Length" optionList={classLengthList}/><br/>
        <RadioGroup radioGroupLabel="Setlist Version" optionList={setlistVersionList}/><br/>
        <CheckboxOption checkboxLabel="Include Arm Track"/>
        <button type="submit" value="Generate"/>
      </form>
    </div>
  );
}

function PoundSetlist({ setlistData, difficulty, classLength, setlistVersion, includeArmTrack }) {
  let setlist = [];
  setlistData.forEach((trackData) => {
    let level = trackData.contains('level') ? trackData.level : null;
    setlist.push(
      <li><span><PoundTrack name={trackData.name} artist={trackData.artist} type={trackData.type} level={level}/></span><span><button type="button">Replace</button></span></li>
    );
  });

  return (
    <div>
      <ol>
        { setlist }
      </ol>
    </div>
  );
}

function PomReplace({ setlistData, oldTrack, replacementOptions, onReplacementTrackChange, onSetlistChange }) {
  let replacementRadioOptions = [];

  for(i in replacementOptions) {
    id = "track" + i;
    value = replacementOptions[i];
    label = replacementOptions[i].name + " by " + replacementOptions[i].artist;
    replacementRadioOptions.push(<p><RadioOption id={id} name={id} value={value} label={value}/></p>);
  }

  return(
    <div>
      <form>
        <h3>Which song would you like to replace {oldTrack.name} by {oldTrack.artist} with?</h3>
        {replacementRadioOptions}
        <button type="submit" value="Replace"/>
      </form>
    </div>
  );
}

function PoundReplace({ setlistData, oldTrack, replacementOptions, onReplacementTrackChange, onSetlistChange }) {
  let replacementRadioOptions = [];

  for(i in replacementOptions) {
    id = "track" + i;
    value = replacementOptions[i];
    label = replacementOptions[i].name + " by " + replacementOptions[i].artist;
    replacementRadioOptions.push(<p><RadioOption id={id} name={id} value={value} label={value}/></p>);
  }

  return(
    <div>
      <form>
        <h3>Which {oldTrack.type} Level {oldTrack.level} would you like to replace {oldTrack.name} by {oldTrack.artist} with?</h3>
        {replacementRadioOptions}
        <button type="submit" value="Replace"/>
      </form>
    </div>
  );
}

function PomSetlistGeneratorSection({ setlistData }) {
  const [classLength, setClassLength] = useState("");

  return(
    <div>
      <span><h2>Setlist</h2></span><span><h2>Settings</h2></span><br/>
      <span><PomSetlist setlsitData={setlistData} classLength={classLength}/></span>
      <span><PomSettingsForm onClassLengthChange={setClassLength}/></span>
    </div>
  );
}

function PoundSetlistGeneratorSection({ setlistData }) {
  const [difficulty, setDifficulty] = useState("");
  const [classLength, setClassLength] = useState("");
  const [setlistVersion, setSetlistVersion] = useState("A");
  const [includeArmTrack, setIncludeArmTrack] = useState(true);

  return(
    <div>
      <span><h2>Setlist</h2></span><span><h2>Settings</h2></span><br/>
      <span><PoundSetlist setlistData={setlistData} difficulty={difficulty} classLength={classLength} setlistVersion={setlistVersion} includeArmTrack={includeArmTrack}/></span>
      <span><PoundSettingsForm onDifficultyChange={setDifficulty} onClassLengthChange={setClassLength} onSetlistVersionChange={setSetlistVersion} onIncludeArmTrackChange={setIncludeArmTrack}/></span>
    </div>
  );
}

function ReplaceAlert() {
  return(
    <div>
      <h3>Replace manually or automatically?</h3><br/>
      <span><button type="button">Manual</button></span><span><button type="button">Automatic</button></span>
    </div>
  );
}

function ClassSelector() {
  return(
    <div>
      <span><button type="button">POUND</button></span><span><button type="button">PomSquad</button></span>
    </div>
  );
}

function MainContentSection({ replacementOptions }){
  const [setlistData, setSetlistData] = useState([]);
  const [replacementTrackData, setReplacementTrackData] = useState({});
  
  return(
    <div>
        <PoundSetlistGeneratorSection setlistData={setlistData}/>
        <PomSetlistGeneratorSection setlistData={setlistData}/>
        <PoundReplace setlistData={setlistData} oldTrack={track} replacementOptions={replacementOptions} onReplacementTrackChange={setReplacementTrackData} onSetlistChange={setSetlistData}/>
        <PomReplace setlistData={setlistData} oldTrack={track} replacementOptions={replacementOptions} onReplacementTrackChange={setReplacementTrackData} onSetlistChange={setSetlistData}/>
    </div>
  );
}

function App() {
  return (
    <div>
      <header>
        <h2>Setlist Generator</h2><br/>
        <ClassSelector/>
      </header>
      <body>
        <MainContentSection replacementOptions={REPLACEMENTOPTIONS}/>
      </body>
    </div>
  );
}

const REPLACEMENTOPTIONS= [
  {"name":"DummySong1", "artist":"DummyArtist1","Type":"DummyType1", "Level":"DummyLevel1"},
  {"name":"DummySong2", "artist":"DummyArtist2","Type":"DummyType1", "Level":"DummyLevel1"}
]

export default App;
