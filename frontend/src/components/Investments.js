import React, { Component } from 'react';
import axios from "axios";
import Navbar from "./Navbar";

 class Investments extends Component {
     constructor(props) {
        super(props);
        this.state = {
          stocks: []
        }
     }


     
    render() {
        return (
            <div>
                <Navbar/>
                <div className="container">

                </div>
                
            </div>
        )
    }
}

export default Investments;