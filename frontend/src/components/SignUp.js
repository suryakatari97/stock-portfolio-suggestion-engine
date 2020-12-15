import React, { Component } from 'react';
import axios from "axios";
import swal from 'sweetalert';
import { Redirect } from 'react-router'

class SignUp extends Component {
    constructor() {
    super();
    this.state = {
      firstName: '',
      lastName:'',
      email: '',
      password: '',
      errors: {},
      redirect: false
    };

    this.onChange = this.onChange.bind(this);
    this.onSubmit = this.onSubmit.bind(this);
  }

  onChange(e) {
    this.setState({ [e.target.name]: e.target.value });
  }

  onSubmit(e) {
    e.preventDefault();
    console.log("In Submit post");
    const newUser = {
        firstName:this.state.firstName,
        lastName:this.state.lastName,
      email: this.state.email,
      password: this.state.password,
    };
     axios("/signup", {
      method: "post",
      data: newUser,
    })
      .then((response) => {
        console.log("THIS IS SIGNUP",response);
        if (response.status === 200) {
          swal({
            title: "Success",
            text: "added successfully",
            icon: "success",
            button: "OK",
          })
            .then(() => {
              this.setState({ redirect: true })
            })
            .catch((error) => console.log(error.response.data));
        } else if (response.status === 500) {
            console.log("Ins stautus 500");
          swal({
            title: "Sorry",
            text: "already exists",
            icon: "error",
            button: "OK",
          })
            .catch((error) => console.log(error.response.data));
        }
      })
      .catch((error) => {
        console.log("add project not 2xx response");
        swal({
            title: "Sorry",
            text: "already exists",
            icon: "error",
            button: "OK",
          })
            .catch((error) => console.log(error.response.data));
      });

    // console.log(newUser);
    // this.props.registeruser(newUser,this.props.history);
  }
    render() {
        const { redirect } = this.state;

     if (redirect) {
       return <Redirect to='/login'/>;
     }
        return (
            <div className="register">
        <div className="container">
          <div className="row">
            <div className="col-md-8 m-auto">
              <h1 className="display-4 text-center">Sign Up</h1>
              <p className="lead text-center">
                Create your account
              </p>
              <form noValidate onSubmit={this.onSubmit}>
                <div className="form-group">
                  <input
                    type="text"
                    placeholder="firstName"
                    name="firstName"
                    value={this.state.firstName}
                    onChange={this.onChange}
                  />
                </div>
                <div className="form-group">
                  <input
                    type="text"
                    placeholder="lastName"
                    name="lastName"
                    value={this.state.lastName}
                    onChange={this.onChange}
                  />
                </div>
                <div className="form-group">
                  <input
                    type="email"
                    placeholder="Email Address"
                    name="email"
                    value={this.state.email}
                    onChange={this.onChange}
                  />
                  <small className="form-text text-muted">
                  </small>
                </div>
                <div className="form-group">
                  <input
                    type="password"
                    placeholder="Password"
                    name="password"
                    value={this.state.password}
                    onChange={this.onChange}
                  />
                </div>
                <input type="submit" className="btn btn-info btn-block mt-4" />
              </form>
            </div>
          </div>
        </div>
      </div>
        )
    }
}


export default SignUp;
