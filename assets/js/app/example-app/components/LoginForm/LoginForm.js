import React from 'react';

import './style.scss';
import LogoImg from '../../../../../images/sign-in-with-github.png';
import LogoImg2x from '../../../../../images/sign-in-with-github@2x.png';


class LoginForm extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      color: 'black',
    };
  }

  render() {
    return (
      <div className="login-form">
        <div className="button">
          <img src={LogoImg} srcSet={`${LogoImg2x} 2x`} />
        </div>
      </div>
    );
  }
}

export default LoginForm;
