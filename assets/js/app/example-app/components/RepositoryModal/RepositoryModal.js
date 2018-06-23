import React from 'react';

import './style.scss';


class RepositoryModal extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      // color: 'black',
    };
  }

  render() {
    return (
      <div className="repository-modal">
        <div className="modal">
          <div className="title">Add Repository</div>
          <div className="label">owner/name</div>
          <div className="input">
            <input type="text" value="tcostam/" />
          </div>
          <div className="message">repository not found.</div>
          <div className="buttons">
            <div className="button">Save</div>
            <div className="button -red">Cancel</div>
          </div>
        </div>
      </div>
    );
  }
}

export default RepositoryModal;
