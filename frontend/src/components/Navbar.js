import React, { Component } from 'react';

 class Navbar extends Component {
     handleLogout(e) {
    // e.preventDefault();
    // this.props.logoutUser();
    // this.props.clearUser();
    // window.location.href = "/";
  }
    render() {
        return (
            <div>
                <nav className="navbar navbar-expand-sm navbar-dark bg-dark mb-4">
        <div className="container">
          <a className="navbar-brand" href="#">
            Stocks
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-toggle="collapse"
            data-target="#mobile-nav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <a
                  className="nav-link"
                  href="/"
                  onClick={this.handleLogout.bind(this)}
                >
                  Logout
                </a>
              </li>
            </ul>
          </div>
        
      </nav>
                
            </div>
        )
    }
}

export default Navbar;
