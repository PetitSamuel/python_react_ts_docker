import React from 'react';
import './App.css';
import image from './img/nath.jpg';
import GoogleLogin, { GoogleLoginResponse, GoogleLoginResponseOffline } from 'react-google-login';

const App = () => {
  return (
    <div className="App">
      <div className="App-header">
        <button onClick={test}>click me </button>
        <GoogleLogin
        // todo : env vars for this
          clientId={"271218736019-k35pfnkhf8rmhu3go174m29dclolfh6c.apps.googleusercontent.com"}
          buttonText="Login"
          onSuccess={responseGoogle}
          onFailure={responseGoogle}
          cookiePolicy={'single_host_origin'}
        />
        <div id="side-bar">
          <div id="line">
            <img src={image} alt="header-img" />
            <p>Samuel Petit</p>
          </div>
        </div>
        <div id="main">
          <p>Some stuff here :)</p>
        </div>
      </div>
    </div>
  );
}

export default App;


function isOnline(obj: any): obj is GoogleLoginResponse {
  return obj.googleId !== undefined
}
async function responseGoogle(response: GoogleLoginResponse | GoogleLoginResponseOffline) {
  if (!isOnline(response)) {
    // todo handle offline response type
    console.log("offline response type not handled yet")
    return;
  }
  let auth = response.getAuthResponse();
  let profile = response.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.

  try {
    console.log(JSON.stringify({
      id_token: auth.id_token,
      first_name: profile.getGivenName(),
      last_name: profile.getFamilyName(),
      email: profile.getEmail(),
      image: profile.getImageUrl(),
    }));
    const response = await fetch(`http://localhost:5000/api/auth/google`, {
      method: "post",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
      body: JSON.stringify({
        id_token: auth.id_token,
        // first_name: profile.getGivenName(),
        // last_name: profile.getFamilyName(),
        // email: profile.getEmail(),
        // image: profile.getImageUrl(),
      })
    });
    console.log(response);
  } catch (ex) {
    console.log(ex);
  }
}


async function test() {
  fetch(`http://localhost:5000/`)
    .then(res => res.json())
    .then(res => {
      console.log(res);
    });
}
