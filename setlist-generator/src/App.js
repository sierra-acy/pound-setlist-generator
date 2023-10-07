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

function RadioGroup({ radioGroupLabel, name, optionsList }) {
  let options = optionsList.map(option => <RadioOption key={option.toLowerCase()} id={option.toLowerCase()} name={name} value={option.toLowerCase()} label={option} />)
  
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
      <input type="checkbox" id={name.toLowerCase()} name={name} value={value} />
      <label htmlFor={name}>{label}</label>
    </div>
  );
}

function Track({ name, artist, type, level }) {
  return(
    <>{type ? type : ""} {level ? level : ""} { type || level ? ":" : ""} {name} by {artist}</>
  );
}

function Settings( { classType, setSetlistData, setChosenSettings }) {

  function handleSubmit(e) {
    e.preventDefault();

    let elements = e.target.elements
    let endpoint = '';
    let queryParams = [];
    let currChosenSettings = {};
    if(classType === "pound") {
      // generate pound setlist
      currChosenSettings = {
        "difficulty":elements['difficultySetting'].value,
        "length":elements['lengthSetting'].value,
        "version":elements['versionSetting'].value,
        "includeArmTrack":elements['includeArmTrackSetting'].value
      };
      setChosenSettings(currChosenSettings);

      endpoint = '/pound-setlist';
      queryParams.push('difficulty=' + currChosenSettings['difficulty']);
      queryParams.push('length=' + currChosenSettings['length']);
      queryParams.push('version=' + currChosenSettings['version']);
      queryParams.push('includeArmTrack=' + currChosenSettings['includeArmTrack']);
    } else if(classType === "pom") {
      // generate pom setlist
      currChosenSettings = {
        "length":elements['lengthSetting'].value
      };
      setChosenSettings(currChosenSettings);

      endpoint = '/pom-setlist';
      queryParams.push('length=' + currChosenSettings['length']);
    } else {
      console.log("classType not found");
    }

    if(queryParams.length > 0) {
      endpoint += '?' + queryParams.join('&');
    }

    fetch(endpoint).then(res => res.json()).then(data => {
      setSetlistData(data);
    });
  }

  let settingsData = [];
  if (classType === 'pound') {
    settingsData = [<RadioGroup key="difficulty" radioGroupLabel="Class Difficulty" name="difficultySetting" optionsList={["Beginner","Advanced"]}/>,
    <RadioGroup key="length" radioGroupLabel="Class Length" name="lengthSetting" optionsList={["15","30","45"]}/>,
    <RadioGroup key="version" radioGroupLabel="Setlist Version" name="versionSetting" optionsList={["A","B"]}/>,
    <CheckboxOption key="includeArmTrack" label="Include Arm Track" name="includeArmTrackSetting" value={false}/>]
  } else if (classType === 'pom') {
    settingsData = [<RadioGroup key="length" radioGroupLabel="Class Length" name="lengthSetting" optionsList={["20","30","50"]}/>];
  }

  return(
    <div>
      <h2>Settings</h2>
      <form onSubmit={handleSubmit}>
        {settingsData}
        <button type="submit" value="Generate">Generate</button>
      </form>
    </div>
  );
}

function Setlist({ setlistData, setReplacementOptions, setIsReplace, setTrackToReplace, classType, chosenSettings }) {
  function handleReplace(trackData, e) {
    setTrackToReplace(trackData);

    // generate list of replacements using track data
    let endpoint = '';
    let body = {};
    if(classType === "pound") {
      endpoint = '/pound-replacement-options'
      body['setlist'] = setlistData;
      body['trackNum']  = e.target.parentNode.id;
      body['includeArmTrack'] = chosenSettings['includeArmTrack'];
      body["difficulty"] = chosenSettings['difficulty'];
      body["length"] = chosenSettings['length'];
      body["version"] = chosenSettings['version'];
    } else if(classType === "pom") {
      endpoint = '/pom-replacement-options'
      body['setlist'] = setlistData;
      body['trackNum']  = e.target.parentNode.id;
    } else {
      console.log("class type not found");
    }

    // POST request to be able to send json body
    const request = new Request(endpoint, {
      method: "POST",
      body: JSON.stringify(body),
      headers: new Headers({'content-type': 'application/json'}),
    });

    fetch(request).then(res => res.json()).then(data => {
      if(data.length === 0) {
        let innerHTML = e.target.parentNode.innerHTML;
        let text = innerHTML.substring(0, innerHTML.indexOf("<"));
        alert("There are no valid replacement options for " + text + ".");
      } else {
        setReplacementOptions(data);
        setIsReplace(true);
      }
    });
  }

  let id = 1;
  return (
    <div>
      <h2>Setlist</h2>
      <ol>
        {setlistData.map(trackData => {
          let level = "level" in trackData ? trackData.level : false;
          let type = "type" in trackData ? trackData.type : false;
          return <li id={id++} key={'li'+trackData.id}><Track key={trackData.id} name={trackData.name} artist={trackData.artist} type={type} level={level} /><button type="button" onClick={(e) => handleReplace(trackData, e)}>Replace</button></li>
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

function SetlistGeneratorSection({ classType, setlistData, setSetlistData, setReplacementOptions, setIsReplace, setTrackToReplace, chosenSettings, setChosenSettings }) {
  return(
    <div> 
      <div className="generator">
        <Setlist setlistData={setlistData} setReplacementOptions={setReplacementOptions} setIsReplace={setIsReplace} setTrackToReplace={setTrackToReplace} classType={classType} chosenSettings={chosenSettings}/>
        <Settings classType={classType} setSetlistData={setSetlistData} setChosenSettings={setChosenSettings}/>
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
  const [chosenSettings, setChosenSettings] = useState({});
  
    let section = <></>
    if(isReplace) {
      section = <ReplaceSection setlistData={setlistData} replacementOptions={replacementOptions} onSetlistChange={setSetlistData} setIsReplace={setIsReplace} trackToReplace={trackToReplace} setSetlistData={setSetlistData} classType={classType}/>;
    } else if(classType.length !== 0) {
      section = <SetlistGeneratorSection classType={classType} setlistData={setlistData} setSetlistData={setSetlistData} setReplacementOptions={setReplacementOptions} setIsReplace={setIsReplace} setTrackToReplace={setTrackToReplace} chosenSettings={chosenSettings} setChosenSettings={setChosenSettings}/>
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
        <h2 onClick={() => setClassType("")}>Setlist Generator</h2><br/>
        <ClassSelector handleChooseClass={handleChooseClass}/>
      </header>
      <MainContentSection key={classType} classType={classType}/>
    </div>
    </React.StrictMode>
  );
}
export default App;
