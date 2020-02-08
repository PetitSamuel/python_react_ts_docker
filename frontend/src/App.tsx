import React from 'react';
import './App.css';
import image from './img/nath.jpg';

const App = () => {
  return (
    <div className="App">
      <div className="App-header">
        <div id="side-bar">
          <div id="line">
            <img src={image} alt="header-img" />
            <p>Samuel Petit</p>
          </div>
        </div>
        <div id="main">
          <p>Some stuff here :)</p>
          <button type="submit" onClick={handleInputSubmit}>click me</button>
        </div>
      </div>
    </div>
  );
}

export default App;

function testt() {
  console.log("change lel");
}
async function test() {
  fetch(`http://localhost:5000/test`)
    .then(res => res.json())
    .then(res => {
      console.log(res)
    });
}

function handleInputSubmit() {
  var input = document.getElementById('show-tooltip');
  console.log(input);
  
}