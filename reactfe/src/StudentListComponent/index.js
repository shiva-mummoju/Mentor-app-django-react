import React, { Component } from "react";
// import axios from 'axios';
import { Link } from "react-router-dom";

class StudentListComponent extends Component {
  state = {
    students: null,
    token: null
  };

  constructor(props) {
    super(props);
    this.state.students = null;
    this.state.token = props.token;
  }

  componentDidMount = () => {
    console.log("student list mount called");
    console.log(this.props.match.params);
    console.log(this.props.location.state);
    if (this.state.token) {
      console.log(this.props.match);
      fetch(
        "http://127.0.0.1:8000/api/college/" +
          this.props.match.params.collegeid +
          "/students/",
        {
          method: "GET",
          headers: {
            "content-type": "application/json",
            Authorization: "JWT " + this.state.token
          }
        }
      )
        .then(response => response.json())
        .then(responsejson => {
          console.log(responsejson);

          this.setState(prev => ({
            students: responsejson,
            token: prev.token
          }));
        });
    }
  };

  render() {
    return (
      // <Router>
      <React.Fragment>
        <table className="table">
          <thead class="thead-dark">
            <tr>
              <th>Name</th>
              <th>email</th>
              <th>db_folder</th>
            </tr>
          </thead>

          {this.state.students &&
            this.state.token &&
            this.state.students.map(student => {
              console.log(student);
              return (
                <tr>
                  <td>
                    <Link
                      to={`/react/college/${
                        this.props.match.params.collegeid
                      }/students/${student.id}`}
                    >
                      {student.name}
                    </Link>
                  </td>
                  <td>{student.email}</td>
                  <td>{student.db_folder}</td>
                </tr>
              );
            })}
        </table>
        {/* <Route exact path={`/react/college/:collegeid/`} component={StudentListComponent}  /> */}
      </React.Fragment>
      // </Router>
    );
  }
}

export default StudentListComponent;
