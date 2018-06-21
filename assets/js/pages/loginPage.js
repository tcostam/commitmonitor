import React from 'react';
import ReactDOM from 'react-dom';
import AppContainer from '../app/example-app';


const title = 'Start ' +
              "change the app's name below to test hot reloading)";

ReactDOM.render(<AppContainer>{title}</AppContainer>, document.getElementById('react-app'));
