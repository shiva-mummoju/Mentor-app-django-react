import React, { Component } from "react";
// import axios from 'axios';
// import {  Link } from "react-router-dom";

class StudentDetailComponent extends Component {
  state = {
    student: null,
    result: []
  };

  componentDidMount = () => {
    console.log("student list reached");
    console.log(this.props.match.params.collegeid);
    console.log(this.props.match.params.studentid);

    fetch(
      "http://127.0.0.1:8000/api/college/" +
        this.props.match.params.collegeid +
        "/students/" +
        this.props.match.params.studentid +
        "/"   
    )
      .then(response => response.json())
      .then(responsejson => {
        console.log(responsejson);

        this.setState({
          student: responsejson,
          result: responsejson.mocktest
        });
      });
  };

  render() {
    return (
      <React.Fragment>
        <table className="table">
          <thead class="thead-dark">
            <tr>
              <th>Problem1</th>
              <th>Problem2</th>
              <th>Problem3</th>
              <th>Problem4</th>
              <th>Total</th>
            </tr>
          </thead>

          <tr>
            <td>{this.state.result.problem1}</td>
            <td>{this.state.result.problem2}</td>
            <td>{this.state.result.problem3}</td>
            <td>{this.state.problem4}</td>
            <td>{this.state.mocktest.totals}</td>
          </tr>
        </table>
      </React.Fragment>
    );
  }
}

export default StudentDetailComponent;
