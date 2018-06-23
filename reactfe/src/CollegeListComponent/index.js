import React, { Component } from 'react';
import axios from 'axios';
import StudentListComponent, { } from './../StudentListComponent/index';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

class CollegeListComponent extends Component{
    state = {
        collegename : 'not available',
        location : 'not available',
        acronym : 'not available',
        contact: 'not available',
    }

    constructor(props){
        super(props);
        console.log(props.match);
        this.state = {
            id: props.id,
            collegename : props.collegename,
            location : props.location,
            acronym : props.acronym,
            contact : props.contact,
        }
    }



    render(){
        return (

            <Router>
            <React.Fragment>
            <tr>
                <td> <Link  to={`/react/college/${this.state.id}`}>{this.state.collegename} </Link></td>
                <td> {this.state.location}  </td>
                <td> {this.state.acronym} </td>
                <td> {this.state.contact}  </td>
            </tr>
            <Route  exact path={`/react/college/:collegeid`} component={StudentListComponent}  />
            </React.Fragment>
          </Router>
        
        )
    }

}


export default CollegeListComponent;