import React from 'react';

import './style.scss';


class PageSelector extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // color: 'black',
    };
  }

  render() {
    const pages = [];
    for (let i = 0; i < this.props.pagesCount; i++) {
      if (this.props.currentPage == i) {
        pages.push(<div className="page -active" onClick={this.props.onPageSelectClick} key={i}>{i + 1}</div>);
      } else {
        pages.push(<div className="page" onClick={this.props.onPageSelectClick} key={i}>{i + 1}</div>);
      }
    }

    return (
      <div>
        <div className="pages-container">
          { pages }
        </div>
      </div>
    );
  }
}

export default PageSelector;
