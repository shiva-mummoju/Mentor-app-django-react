import React, { Component } from "react";
// import StudentListComponent from "./../StudentListComponent/index";
import { Link } from "react-router-dom";

class Colleges extends Component {
  state = {
    colleges: null,
    token: null
  };

  constructor(props) {
    super(props);
    this.state.colleges = null;
    this.state.token = props.token;
  }

  componentDidMount = () => {
    console.log("Colleges did mount called", this.state);
    if (this.state.token) {
      // console.log(this.getCookie("JWT"));
      fetch("http://127.0.0.1:8000/api/college/", {
        method: "GET",
        headers: {
          "content-type": "application/json",
          Authorization: "JWT " + this.state.token
        }
      })
        .then(response => response.json())
        .then(responsejson => {
          console.log(responsejson);
          this.setState(prev => ({
            colleges: responsejson,
            token: prev.token
          }));

          console.log("After getting the colleges", this.state);
        });
    }
  };

  render() {
    console.log("Colleges render called", this.state);
    return (
      // <Router>
      <React.Fragment>
        <table className="table">
          <thead className="thead-dark">
            <tr>
              <th>Name</th>
              <th>Location</th>
              <th>Acronym</th>
              <th>Contact</th>
            </tr>
          </thead>

          {this.state.colleges &&
            this.state.token &&
            this.state.colleges.map(college => {
              console.log(college);
              return (
                <tr>
                  <td>
                    <Link to={`/react/college/${college.id}/`}>
                      {college.name}
                    </Link>

                    {/* <Link
                      to={{
                        pathname: `/react/college/${college.id}/`,
                        state: { token: this.state.token }
                      }}
                    >
                      {college.name}
                    </Link> */}
                  </td>
                  <td>{college.location}</td>
                  <td>{college.acronym}</td>
                  <td>{college.contact}</td>
                </tr>
              );
            })}
        </table>
      </React.Fragment>
    );
  }
}

export default Colleges;
