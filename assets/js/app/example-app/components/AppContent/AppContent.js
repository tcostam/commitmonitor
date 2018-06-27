import React from 'react';

import './style.scss';

class AppContent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // aaa
    };
  }

  render() {
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
            {this.props.commits.map(item => <li key={item.id}>{item.name}</li>)}
          </ul>
        </div>
      </div>
    );
  }
}

export default AppContent;
