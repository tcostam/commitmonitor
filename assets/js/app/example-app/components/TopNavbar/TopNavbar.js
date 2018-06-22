import React from 'react';

import './style.scss';

const avatarStyle = {
  backgroundImage: 'url(' + context.avatar + ')'
};

class TopNavbar extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // color: 'black',
    };
  }

  render() {


    return (
      <div className="top-navbar">
        <div className="container">
          <div className="logo">
            <span>commit</span>monitor
          </div>
          <div className="avatar">
            <div className="image" style={avatarStyle}>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default TopNavbar;
