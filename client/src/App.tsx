import React from 'react';
import './App.css';
import image from './img/nath.jpg'; 

const App = () => {
  return (
    <div className="App">
      <div className="App-header">
      <div id="side-bar">
        <div id="line">
          <img src={image} />
          <p>column lol</p>
        </div>
      </div>
      <div id="main">
        <p>column lol</p>
      </div>
      </div>
    </div>
  );
}
//      <button onClick={test}> Hey ! </button>


export default App;

async function test() {
  fetch(`http://localhost:5000/test`)
      .then(res => res.json())
      .then(res => {
          console.log(res)
      });
} 