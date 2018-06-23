import React from 'react';
// import PropTypes from 'prop-types';

import './style.scss';
import TopNavbar from '../TopNavbar';
import AppContent from '../AppContent';
import RepositoryModal from '../RepositoryModal';


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
        <RepositoryModal />
      </div>
    );
  }
}

export default AppContainer;
