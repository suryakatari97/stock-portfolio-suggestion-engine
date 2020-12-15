import React, { Component } from 'react';
import axios from "axios";
import swal from 'sweetalert';
import { Redirect } from 'react-router'



 class Login extends Component {
     constructor() {
        super();
        this.state = {
            email: '',
            password: '',
            userType: '',
            errors: {},
            redirect: false
        };

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChange(e){
        this.setState({[e.target.name]: e.target.value});
    }

    onSubmit(e){
        e.preventDefault();
        const user = {
            email : this.state.email,
            password : this.state.password,
        };
        axios("/login", {
      method: "post",
      data: user,
    })
      .then((response) => {
        console.log("THIS IS LOGIN RESPONSE",response);
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
            console.log("IN STATUS 500");
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
            text: "Invalid Credentials",
            icon: "error",
            button: "OK",
          })
            .catch((error) => console.log(error.response.data));
      });
        }
    render() {
    const { redirect } = this.state;
     if (redirect) {
       return <Redirect to='/home'/>;
     }
        return (
            <div className="login">
            <div className="container">
              <div className="row">
                <div className="col-md-8 m-auto">
                  <h1 className="display-4 text-center">Log In</h1>
                  <p className="lead text-center">Sign in to your Stock Portfolio</p>
                  <form onSubmit={this.onSubmit}>
                        <div className="form-group">
                        <input type="email" 
                            className="form-control form-control-lg"
                            placeholder="Email Address" 
                            name="email" 
                            value={this.state.email} 
                            onChange={this.onChange} />      
                    </div>
                    <div className="form-group">
                      <input type="password" 
                        className="form-control form-control-lg"
                        placeholder="Password" 
                        name="password" 
                        value={this.state.password} 
                        onChange={this.onChange}/>
                    </div>
                    <div>               
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

export default Login;
