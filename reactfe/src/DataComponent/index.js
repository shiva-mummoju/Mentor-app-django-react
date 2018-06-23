import React, { Component } from 'react';
import axios from 'axios';

class DataComponent extends Component{


    state = {
        name : 'noname',
        email : 'not available',
        db_folder: 'not available',
    }

    constructor(props){
        super(props);
    }



    componentDidMount(){
        axios.get('http://127.0.0.1:8000/api/college/912/students/' + this.props.studentid +'/').then( (response) => 
        {
            this.setState({
                name : response.data.name,
                email : response.data.email,
                db_folder : response.data.db_folder,
            }) ;
            console.log(response.data);
         }
    );}


    render(){
        console.log("data component render function has been called");
        return  ( <tr>
            <td>{ this.state.name }</td>
            <td>{ this.state.email }</td>
            <td>{ this.state.db_folder }</td>
            </tr> )
    }
}


export default DataComponent;