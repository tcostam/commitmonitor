import React from 'react';
import Moment from 'moment';

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
          <div className="page-header">
            <div className="text">All Repositories</div>
            <div className="icon" onClick={this.props.onAddRepositoryClick}>
              <img src={"/static/images/addRepoImage.png"} srcSet={`${"/static/images/addRepoImage@2x.png"} 2x`} />
            </div>
          </div>

          <ul>
            {this.props.commits.map(item => <li key={item.id}>{item.sha},
              {item.message}, {item.repository.name}, {item.github_author_name}, {Moment(item.date).format('MM/DD/YYYY')}</li>)}
          </ul>
        </div>
      </div>
    );
  }
}

export default AppContent;
