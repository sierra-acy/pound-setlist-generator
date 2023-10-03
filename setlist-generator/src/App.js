import React, { useState } from "react";
import "./App.css";


function RadioOption({ id, name, value, label }) {
  return (
    <div>
      <input type="radio" key={id} id={id} name={name} value={value}/>
      <label htmlFor={id}>{label}</label>
    </div>
  );
}

function RadioGroup({ radioGroupLabel, optionsList }) {
  let options = optionsList.map(option => <RadioOption key={option} id={option} name={radioGroupLabel} value={option} label={option} />)
  
  return (
    <div>
      <p>{radioGroupLabel}:</p>
      {options}
    </div>
  );
}

function CheckboxOption({ label, name, value }) {
  return(
    <div>
      <input type="checkbox" id={name} name={name} value={value} />
      <label htmlFor={name}>{label}</label>
    </div>
  );
}

function Track({ name, artist, type, level }) {
  return(
    <>{type ? type : ""} {level ? level : ""} { type || level ? ":" : ""} {name} by {artist}</>
  );
}

function Settings( { classType, settingsData, setSetlistData }) {

  function handleSubmit(e) {
    e.preventDefault();

    let endpoint = '';
    if(classType === "pound") {
      // generate pound setlist
      endpoint = 'pound-setlist';
    } else if(classType === "pom") {
      // generate pom setlist
      endpoint = 'pom-setlist';
  } else {
      console.log("classType not found");
    }

    fetch('/' + endpoint).then(res => res.json()).then(data => {
      console.log("setting setlistdata in Settings");
      setSetlistData(data);
    });
  }

  let settings = settingsData.map(setting => {
    if(setting.type === "radio") {
      return <RadioGroup key={setting.label} radioGroupLabel={setting.label} optionsList={setting.options} />
    } else if (setting.type === "checkbox") {
      return <CheckboxOption key={setting.label} label={setting.label} name={setting.name} value={false}/>
    } else {
      return <></>
    }});

  return(
    <div>
      <h2>Settings</h2>
      <form onSubmit={handleSubmit}>
        {settings}
        <button type="submit" value="Generate">Generate</button>
      </form>
    </div>
  );
}

function Setlist({ setlistData, setReplacementOptions, setIsReplace, setTrackToReplace, classType }) {
  function handleReplace(trackData) {
    setTrackToReplace(trackData);
    // generate list of replacements using track data
    let endpoint = '';
    if(classType === "pound") {
      endpoint = '/pound-replacement-options'
    } else if(classType === "pom") {
      endpoint = '/pom-replacement-options'
    } else {
      console.log("class type not found");
    }

    fetch(endpoint).then(res => res.json()).then(data => {
      console.log("setting replacementoptions and isreplace in Setlist");
      setReplacementOptions(data);
      setIsReplace(true);
    })
  }

    return (
      <div>
        <h2>Setlist</h2>
        <ol>
          {setlistData.map(trackData => {
            let level = "level" in trackData ? trackData.level : false;
            let type = "type" in trackData ? trackData.type : false;
            return <li key={trackData.id}><Track name={trackData.name} artist={trackData.artist} type={type} level={level}/><button type="button" onClick={() => handleReplace(trackData)}>Replace</button></li>
          })}
        </ol>
      </div>
    );
  }

function ReplaceSection ({ trackToReplace, replacementOptions, setlistData, setSetlistData, setIsReplace, classType }) {

  function handleSubmit(e) {
    e.preventDefault();
    // newTrackId = e.target.id
    // find index of trackToReplace in setlist data
    // map( track => { if track.id === trackToReplace.id{ return getTrack(newTrackId)}} )???
    // POST to update backend -- retuns updated??
  
    const requestOptions = {
      method: 'PUT',
      body: trackToReplace
    };

    let endpoint = '';
    if(classType === 'pound') {
      endpoint = '/pound-setlist';
    } else if(classType === 'pom') {
      endpoint = '/pom-setlist';
    } else {
      console.log('classtype not found');
    }

    fetch(endpoint, requestOptions).then(res => res.json()).then(data => {
      setSetlistData(data);
      setIsReplace(false);
    });
    
  }

  let prompt = "Which ";
  if("type" in trackToReplace) {
    prompt = prompt.concat(trackToReplace.type + " ");
  }
  if("level" in trackToReplace) {
    prompt = prompt.concat("Level " + trackToReplace.level + " ")
  }
  prompt = prompt.concat("would you like to replace " + trackToReplace.name + " by " + trackToReplace.artist + " with?");

  return(
    <div>
      <form onSubmit={handleSubmit}>
        <h3>{prompt}</h3>
        {replacementOptions.map(track => {
            let value = (track.name + track.artist).toLowerCase().replaceAll(" ", "");
            return <RadioOption key={track.id} id={track.id} name="replaceTrack" value={value} label={track.name + " by " + track.artist} />
          })
        }
        <button type="submit" value="Replace">Replace</button>
      </form>
    </div>
  );
}

function SetlistGeneratorSection({ classType, setlistData, setSetlistData, setReplacementOptions, setIsReplace, setTrackToReplace }) {
  // const [difficulty, setDifficulty] = useState("");
  // const [classLength, setClassLength] = useState("");
  // const [setlistVersion, setSetlistVersion] = useState("");
  // const [includeArmTrack, setIncludeArmTrack] = useState(false);

  let settingsData = [];
  if(classType === "pound") {
    settingsData = TEMP_SETTINGS_DATA_POUND;
  } else if(classType === "pom") {
    settingsData = TEMP_SETTINGS_DATA_POM;
  }

  return(
    <div> 
      <div className="generator">
        <Setlist setlistData={setlistData} setReplacementOptions={setReplacementOptions} setIsReplace={setIsReplace} setTrackToReplace={setTrackToReplace} classType={classType}/>
        <Settings classType={classType} settingsData={settingsData} setSetlistData={setSetlistData}/>
      </div>
    </div>
  );
}

function ClassSelector({ handleChooseClass }) {
  return(
    <div>
      <button type="button" onClick={handleChooseClass} value="pound">POUND</button>
      <button type="button" onClick={handleChooseClass} value="pom">PomSquad</button>
    </div>
  );
}

function MainContentSection({ classType }){
  // visual states:
  // 1. Setlist Generator Section
  // 2. Replace

  const [isReplace, setIsReplace] = useState(false);
  const [setlistData, setSetlistData] = useState([]);
  const [replacementOptions, setReplacementOptions] = useState([]);
  const [trackToReplace, setTrackToReplace] = useState({});
  
    let section = <></>
    if(isReplace) {
      section = <ReplaceSection setlistData={setlistData} replacementOptions={replacementOptions} onSetlistChange={setSetlistData} setIsReplace={setIsReplace} trackToReplace={trackToReplace} setSetlistData={setSetlistData} classType={classType}/>;
    } else if(classType.length !== 0) {
      section = <SetlistGeneratorSection classType={classType} setlistData={setlistData} setSetlistData={setSetlistData} setReplacementOptions={setReplacementOptions} setIsReplace={setIsReplace} setTrackToReplace={setTrackToReplace}/>  
    }

    return section;
}

function App() {
  const [classType, setClassType] = useState(""); //pound or pom

  function handleChooseClass(e) {
    console.log("setting classType in App");
    let shouldContinue = false;
    if(classType != "") {
      shouldContinue = window.confirm("Are you sure you want to switch formats? All progress will be lost. Click \"OK\" to continue.");
    } else {
      shouldContinue = true;
    }
    
    if(shouldContinue)  {
      // clear data
      // set class type to e.target.value
      setClassType(e.target.value);
    }
    
  }

  return (
    <React.StrictMode>
    <div>
      <header className="App-header">
        <h2>Setlist Generator</h2><br/>
        <ClassSelector handleChooseClass={handleChooseClass}/>
      </header>
      <MainContentSection key={classType} classType={classType}/>
    </div>
    </React.StrictMode>
  );
}

const DUMMYREPLACEMENTOPTIONS= [
  {"id":5, "name":"DummySong1", "artist":"DummyArtist1","type":"DummyType1", "level":"DummyLevel1"},
  {"id":6, "name":"DummySong2", "artist":"DummyArtist2","type":"DummyType1", "level":"DummyLevel1"}
]

const TEMP_SETTINGS_DATA_POUND = [
    {"label":"Class Difficulty", "type":"radio", "options":["Beginner", "Intermediate", "Advanced"]},
    {"label":"Class Length", "type":"radio", "options":["15", "30", "45"]},
    {"label":"Setlist Version", "type":"radio", "options":["A", "B"]},
    {"label":"Include Arm Track", "type":"checkbox", "name":"includeArmTrack"}
]

const TEMP_SETTINGS_DATA_POM = [
    {label:"Class Length", type:"radio", options:["15", "30", "50"]}
  ]

export default App;
