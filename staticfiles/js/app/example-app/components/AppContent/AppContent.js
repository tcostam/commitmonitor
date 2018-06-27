import React from 'react';
import Moment from 'moment';

import PageHeader from '../PageHeader';

import './style.scss';

class AppContent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // aaa
    };
  }

  render() {
    Moment.locale('pt-br');

    return (
      <div className="app-content">
        <div className="container">
          <PageHeader selectedRepository={this.props.selectedRepository}
            onAddRepositoryClick={this.props.onAddRepositoryClick}
            onExitRepositoryClick={this.props.onExitRepositoryClick}
          />

          <div className="commits-table">
            <table className="table">
              <thead>
                <tr>
                  <th>Commit ID (sha)</th>
                  <th>Message</th>
                  <th>Repository</th>
                  <th>Author Name</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {this.props.commits.map(item => <tr key={item.id}>
                  <th>{item.sha}</th>
                  <th>{item.message}</th>
                  <th className="repository" onClick={this.props.onViewRepositoryClick} >{item.repository.name}</th>
                  <th>{item.github_author_name}</th>
                  <th>{Moment(item.date).format('MM/DD/YYYY')}</th>
                </tr>)}
              </tbody>
            </table>
          </div>

        </div>
      </div>
    );
  }
}

export default AppContent;
