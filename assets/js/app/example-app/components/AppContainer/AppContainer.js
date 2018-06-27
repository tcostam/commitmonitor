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
      repositories: [],
      commits: [],
      isLoaded: false,
      error: null,
      modalVisible: false,
    };
  }

  componentDidMount() {
    fetch('/api/v1/repositories/?format=json', {
      credentials: 'include',
    })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            repositories: result,
            modalVisible: (result.lenght > 0),
          });
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        },
      );
  }

  render() {
    return (
      <div className="main-container">
        <TopNavbar />
        <AppContent
          onAddRepositoryClick={() => this.setState({ modalVisible: true })}
          commits={this.state.repositories}
        />
        <RepositoryModal
          onHideRepositoryClick={() => this.setState({ modalVisible: false })}
          modalVisible={this.state.modalVisible}
        />
      </div>
    );
  }
}

export default AppContainer;
