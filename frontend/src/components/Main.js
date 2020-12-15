import React, { Component } from 'react';
import { Route } from "react-router-dom";
import LandingPage from "./LandingPage";
import Login from "./Login";
import Register from "./SignUp";
import Home from "./home";

 class Main extends Component {
    render() {
        return (
            <div>
                <Route exact path="/" component={LandingPage} />
                <Route exact path="/login" component={Login} />
                <Route exact path="/register" component={Register} />
                <Route exact path="/home" component={Home} />    
            </div>
        )
    }
}

export default Main;