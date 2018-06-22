import React from 'react';
// import PropTypes from 'prop-types';

import './style.scss';
import TopNavbar from '../TopNavbar';
import AppContent from '../AppContent';


class AppContainer extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // color: 'black',
    };
  }

  render() {
    return (
      <div className="main-container">
        <TopNavbar />
        <AppContent />
      </div>
    );
  }
}

export default AppContainer;
