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
      currentPage: 0,
      perPage: 10,
      pagesCount: 0,
      itemsCount: 0,
    };

    this.onViewRepositoryClickHandler = this.onViewRepositoryClickHandler.bind(this);
    this.onPageSelectClickHandler = this.onPageSelectClickHandler.bind(this);
    this.onExitRepositoryClickHandler = this.onExitRepositoryClickHandler.bind(this);
    this.reloadCommits = this.reloadCommits.bind(this);
  }

  componentDidMount() {
    // modalVisible: (result.length === 0 || false),
    this.reloadCommits();
    window.scrollTo(0, 0);
  }

  onViewRepositoryClickHandler(event) {
    const repositoryName = event.target.innerText;

    this.setState({
      selectedRepository: repositoryName,
      commits: [],
      currentPage: 0,
      isLoaded: false,
    }, () => {
      this.reloadCommits();
      window.scrollTo(0, 0);
    });
  }

  onPageSelectClickHandler(event) {
    const page = event.target.innerText;
    this.setState({
      currentPage: page - 1,
      commits: [],
      isLoaded: false,
    }, () => {
      this.reloadCommits();
      window.scrollTo(0, 0);
    });
  }

  onExitRepositoryClickHandler() {
    this.setState({
      selectedRepository: null,
      commits: [],
      currentPage: 0,
      isLoaded: false,
    }, () => {
      this.reloadCommits();
      window.scrollTo(0, 0);
    });
  }

  reloadCommits() {
    let headers = {};
    let path = null;

    if (this.state.selectedRepository != null) {
      path = '/api/v1/commits/?format=json&repository=' + this.state.selectedRepository;
    } else {
      path = '/api/v1/commits/?format=json';
    }

    fetch(path, {
      credentials: 'include',
      headers: {
        'X-Per-Page': 10,
        'X-Current-Page': this.state.currentPage,
      },
    })
    .then((res) => {
      headers = res.headers;
      return res.json();
    })
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            commits: result,
            currentPage: headers.get('Current-Page'),
            perPage: headers.get('Per-Page'),
            pagesCount: headers.get('Pages-Count'),
            itemsCount: headers.get('Items-Count'),
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
          onPageSelectClick={this.onPageSelectClickHandler}
          onExitRepositoryClick={this.onExitRepositoryClickHandler}
          currentPage={this.state.currentPage}
          pagesCount={this.state.pagesCount}
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
