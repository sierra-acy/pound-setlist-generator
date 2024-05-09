import React, { useState } from "react";
import { Header, Container, Form, Button, List, ListItem,
  ListContent, Icon, FormField, FormRadio, FormCheckbox } from 'semantic-ui-react'
import "./App.css";


function RadioOption({ id, name, value, label, chosen }) {
  return (
      <FormRadio label={label} key={id} id={id} name={name} value={value} defaultChecked={chosen} />
  );
}

function RadioGroup({ radioGroupLabel, name, optionsList, chosen }) {
  let options = optionsList.map(option => <RadioOption key={option.toLowerCase()} id={option.toLowerCase()} name={name}
  value={option.toLowerCase()} label={option} chosen={chosen === option.toLowerCase()} />)
  
  return (
    <FormField required style={{paddingBottom:'2vh'}} >
      <label>{radioGroupLabel}:</label>
      {options}
    </FormField>
  );
}

function CheckboxOption({ label, name, checked }) {
  return(
    <FormCheckbox label={label} id={name.toLowerCase()} name={name} defaultChecked={checked} style={{paddingBottom:'2vh'}} />
  );
}

function Track({ name, artist, type, level }) {
  return(
    <ListContent floated="left">
      <b>{type ? type : ""} {level ? level : ""} { type || level ? ":" : ""}</b> {name} by {artist}
    </ListContent>
  );
}

function Settings({ classType, setSetlistData, setChosenSettings, chosenSettings }) {

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
        "includeArmTrack":elements['includeArmTrackSetting'].checked
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
  let color = 'green';
  if (classType === 'pound') {
    let difficulty = 'beginner';
    let length = '15';
    let version = 'a';
    let includeArmTrack = false;
    if(chosenSettings && Object.keys(chosenSettings).length > 0) {
      difficulty = chosenSettings['difficulty'];
      length = chosenSettings['length'];
      version = chosenSettings['version'];
      includeArmTrack = chosenSettings['includeArmTrack'];
    }
    settingsData = [<RadioGroup key="difficulty" radioGroupLabel="Class Difficulty" name="difficultySetting"
    optionsList={["Beginner","Advanced"]} chosen={difficulty} />,
    <RadioGroup key="length" radioGroupLabel="Class Length" name="lengthSetting" optionsList={["15","30","45"]}
    chosen={length} />,
    <RadioGroup key="version" radioGroupLabel="Setlist Version" name="versionSetting" optionsList={["A","B"]}
    chosen={version} />,
    <CheckboxOption key="includeArmTrack" label="Include Arm Track" name="includeArmTrackSetting"
    checked={includeArmTrack}/>]
  } else if (classType === 'pom') {
    let length = '20';
    if(chosenSettings && Object.keys(chosenSettings).length > 0 ) {
      length = chosenSettings['length'];
    }
    settingsData = [<RadioGroup key="length" radioGroupLabel="Class Length" name="lengthSetting"
    optionsList={["20","30","50"]} chosen={length} />];
    color = 'pink';
  }

  return(
    <div>
      <Header as="h2">Settings</Header>
      <Form onSubmit={handleSubmit}>
        {settingsData}
        <Button color={color} type="submit" value="Generate">Generate</Button>
      </Form>
    </div>
  );
}

function Setlist({ setlistData, setReplacementOptions, setIsReplace, setTrackToReplace, classType, chosenSettings }) {
  function handleReplace(trackData, e) {
    // generate list of replacements using track data
    let endpoint = '';
    let body = {};
    body['trackNum']  = e.target.parentNode.id;
    setTrackToReplace({"trackNum":e.target.parentNode.id, "trackData":trackData});
    if(classType === "pound") {
      endpoint = '/pound-replacement-options'
      body['setlist'] = setlistData;
      body['includeArmTrack'] = chosenSettings['includeArmTrack'];
      body["difficulty"] = chosenSettings['difficulty'];
      body["length"] = chosenSettings['length'];
      body["version"] = chosenSettings['version'];
    } else if(classType === "pom") {
      endpoint = '/pom-replacement-options'
      body['setlist'] = setlistData;
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
  let color = classType === "pound" ? ' inverted green' : 'inverted pink';
  return (
    <div>
      <Header as='h2'>Setlist</Header>
      <List ordered relaxed>
        {setlistData.map(trackData => {
          let level = "level" in trackData ? trackData.level : false;
          let type = "type" in trackData ? trackData.type : false;
          return <ListItem id={id++} key={'li'+trackData.id}>
            <Track key={trackData.id} name={trackData.name} artist={trackData.artist} type={type} level={level} />
            <Button circular icon type="button" onClick={(e) => handleReplace(trackData, e)} title="Replace"
            floated="right" color={color} size="mini">
              <Icon name="sync alternate" style={{pointerEvents:"none"}}/></Button>
          </ListItem>
        })}
      </List>
    </div>
  );
}

function ReplaceSection ({ trackToReplace, replacementOptions, setlistData, setSetlistData, setIsReplace, classType }) {

  function handleSubmit(e) {
    e.preventDefault();

    let endpoint = '';
    let body = {};
    body['trackNum'] = trackToReplace['trackNum'];
    body['setlist'] = setlistData;
    body['newTrackId'] = e.target.elements['replaceTrack'].value;
    if(classType === 'pound') {
      endpoint = '/pound-setlist';
    } else if(classType === 'pom') {
      endpoint = '/pom-setlist';
    } else {
      console.log('classtype not found');
    }

    const requestOptions = {
      method: 'PUT',
      body: JSON.stringify(body),
      headers: new Headers({'content-type': 'application/json'}),
    };

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
  prompt = prompt.concat("would you like to replace " + trackToReplace.name + " by " + trackToReplace.artist + 
  " with?");

  let color = classType === "pound" ? "green" : "pink";
  return(
    <div>
      <Form onSubmit={handleSubmit}>
        <h3>{prompt}</h3>
        {replacementOptions.map(track => {
            return <RadioOption key={track.id} id={track.id} name="replaceTrack" value={track.id}
            label={track.name + " by " + track.artist} />
          })
        }
        <Button color={color} type="submit" value="Replace">Replace</Button>
      </Form>
    </div>
  );
}

function SetlistGeneratorSection({ classType, setlistData, setSetlistData, setReplacementOptions, setIsReplace,
  setTrackToReplace, chosenSettings, setChosenSettings }) {
  return(
      <div className="generator">
        <Setlist setlistData={setlistData} setReplacementOptions={setReplacementOptions} setIsReplace={setIsReplace}
        setTrackToReplace={setTrackToReplace} classType={classType} chosenSettings={chosenSettings}/>
        <Settings classType={classType} setSetlistData={setSetlistData} setChosenSettings={setChosenSettings}
        chosenSettings={chosenSettings}/>
      </div>
  );
}

function ClassSelector({ handleChooseClass }) {
  return(
    <Container>
      <Button type="button" onClick={handleChooseClass} value="pound" color="green">POUND</Button>
      <Button type="button" onClick={handleChooseClass} value="pom" color="pink">PomSquad</Button>
    </Container>
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
      section = <ReplaceSection setlistData={setlistData} replacementOptions={replacementOptions} onSetlistChange={setSetlistData} 
      setIsReplace={setIsReplace} trackToReplace={trackToReplace} setSetlistData={setSetlistData} classType={classType}/>;
    } else if(classType.length !== 0) {
      section = <SetlistGeneratorSection classType={classType} setlistData={setlistData} setSetlistData={setSetlistData} 
      setReplacementOptions={setReplacementOptions} setIsReplace={setIsReplace} setTrackToReplace={setTrackToReplace} 
      chosenSettings={chosenSettings} setChosenSettings={setChosenSettings}/>
    }

    return section;
}

function App() {
  const [classType, setClassType] = useState(""); //pound or pom

  function handleChooseClass(e) {
    console.log("setting classType in App");
    let shouldContinue = false;
    if(classType !== "") {
      shouldContinue = window.confirm("Are you sure you want to switch formats? All progress will be lost. Click " +
      "\"OK\" to continue.");
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
    <Container>
      <Container textAlign="center" id="header">
        <Header as="h2" onClick={() => setClassType("")}>Setlist Generator</Header>
        <ClassSelector handleChooseClass={handleChooseClass} />
      </Container>
      <MainContentSection key={classType} classType={classType}/>
    </Container>
    </React.StrictMode>
  );
}
export default App;
