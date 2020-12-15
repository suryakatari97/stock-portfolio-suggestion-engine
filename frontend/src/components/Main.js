import React, { Component } from 'react';
import { Route } from "react-router-dom";
import LandingPage from "./LandingPage";
import Login from "./Login";
import Register from "./SignUp";
import Home from "./home";
import Investments from "./Investments";
 class Main extends Component {
    render() {
        return (
            <div>
                <Route exact path="/" component={LandingPage} />
                <Route exact path="/login" component={Login} />
                <Route exact path="/register" component={Register} />
                <Route exact path="/home" component={Home} />
                <Route exact path="/investments" component={Investments} />
            </div>
        )
    }
}

export default Main;