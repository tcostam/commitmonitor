import React, { Component } from 'react';

import './style.scss';


class RepositoryModal extends Component {
  constructor(props) {
    super(props);

    this.state = {
      repositoryName: 'tcostam/',
    };
  }

  render() {
    if (this.props.modalVisible) {
      return (
        <div className="repository-modal">
          <div className="modal">
            <div className="title">Add Repository</div>
            <div className="label">owner/name</div>
            <div className="input">
              <input
                type="text"
                value={this.state.repositoryName}
                onChange={event => this.setState({ repositoryName: event.target.value })}
              />
            </div>
            <div className="message">repository not found.</div>
            <div className="buttons">
              <div className="button">Save</div>
              <div className="button -red" onClick={this.props.onHideRepositoryClick}>Cancel</div>
            </div>
          </div>
        </div>
      );
    }

    return null;
  }
}

export default RepositoryModal;
