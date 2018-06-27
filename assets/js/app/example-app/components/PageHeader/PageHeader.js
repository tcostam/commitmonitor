import React from 'react';

import './style.scss';


class PageHeader extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // color: 'black',
    };
  }

  render() {
    if (this.props.selectedRepository != null) {
      return (
        <div className="page-header">
          <div className="back" onClick={this.props.onExitRepositoryClick}>←</div>
          <div className="text">{this.props.selectedRepository}</div>
        </div>
      );
    } else {
      return (
        <div className="page-header">
          <div className="text">All Repositories</div>
          <div className="icon" onClick={this.props.onAddRepositoryClick}>
            <img src={"/static/images/addRepoImage.png"} srcSet={`${"/static/images/addRepoImage@2x.png"} 2x`} />
          </div>
        </div>
      );
    }
  }
}

export default PageHeader;
