import React, { Component } from 'react';
import cookie from 'react-cookies';

import './style.scss';


class RepositoryModal extends Component {
  constructor(props) {
    super(props);

    this.state = {
      repositoryName: context.login + '/',
      errorMessage: '',
    };

    this.saveRepositoryClickHandler = this.saveRepositoryClickHandler.bind(this);
  }

  saveRepositoryClickHandler(event) {
    event.preventDefault();
    const csrftoken = cookie.load('csrftoken');

    fetch('/api/v1/repositories/?format=json', {
      credentials: 'include',
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name: this.state.repositoryName.replace(context.login + '/', '') }),
    })
    .then(
      (result) => {
        if (!result.ok) {
          // XXX TODO Treat different errors and messages
          this.setState({ errorMessage: "Error adding repository." });
        } else {
          this.props.onHideRepositoryClick();
        }
      },
    );
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
            <div className="message">{this.state.errorMessage}</div>
            <div className="buttons">
              <div className="button" onClick={this.saveRepositoryClickHandler} >Save</div>
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
