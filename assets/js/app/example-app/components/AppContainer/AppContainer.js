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
      selectedRepository: null,
      commits: [],
      isLoaded: false,
      error: null,
      modalVisible: false,
    };

    this.onViewRepositoryClickHandler = this.onViewRepositoryClickHandler.bind(this);
    this.onExitRepositoryClickHandler = this.onExitRepositoryClickHandler.bind(this);
    this.reloadCommits = this.reloadCommits.bind(this);
  }

  componentDidMount() {
    fetch('/api/v1/commits/?format=json', {
      credentials: 'include',
    })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            commits: result,
            modalVisible: (result.length === 0 || false),
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

  onViewRepositoryClickHandler(event) {
    const repositoryName = event.target.innerText;
    fetch('/api/v1/commits/?format=json&repository=' + repositoryName, {
      credentials: 'include',
    })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            commits: result,
            modalVisible: (result.length === 0 || false),
            selectedRepository: repositoryName,
          });
          window.scrollTo(0, 0);
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        },
      );
  }

  onExitRepositoryClickHandler() {
    fetch('/api/v1/commits/?format=json', {
      credentials: 'include',
    })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            commits: result,
            modalVisible: (result.length === 0 || false),
            selectedRepository: null,
          });
          window.scrollTo(0, 0);
        },
        (error) => {
          this.setState({
            isLoaded: true,
            error,
          });
        },
      );
  }

  reloadCommits() {
    fetch('/api/v1/commits/?format=json', {
      credentials: 'include',
    })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            commits: result,
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
          selectedRepository={this.state.selectedRepository}
          commits={this.state.commits}
          onAddRepositoryClick={() => this.setState({ modalVisible: true })}
          onViewRepositoryClick={this.onViewRepositoryClickHandler}
          onExitRepositoryClick={this.onExitRepositoryClickHandler}
        />
        <RepositoryModal
          onHideRepositoryClick={() => this.setState({ modalVisible: false })}
          modalVisible={this.state.modalVisible}
          reloadCommits={this.reloadCommits}
          />
      </div>
    );
  }
}

export default AppContainer;
