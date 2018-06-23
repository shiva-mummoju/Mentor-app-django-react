import React, { Component } from "react";
import "./App.css";
import Colleges from "./Colleges/index";
import HeaderComponent from "./HeaderComponent/index";
import { BrowserRouter, Route } from "react-router-dom";
import StudentListComponent from "./StudentListComponent";
import StudentDetailComponent from "./StudentDetailComponent/index";

class App extends Component {
  data = { username: "shiva", password: "shivasairam" };
  state = {
    token: null
  };

  componentDidMount = () => {
    // console.log("Colleges");
    fetch("http://127.0.0.1:8000/login/", {
      method: "POST",
      body: JSON.stringify(this.data),
      headers: { "content-type": "application/json" }
    })
      .then(response => response.json())
      .then(responsejson => {
        console.log("Token recieved", responsejson);
        this.setState({
          token: responsejson.token
        });
        // console.log("after token state of app", this.state);
      });
  };

  render() {
    console.log("render of app called");
    return (
      <div className="App">
        <HeaderComponent />
        <BrowserRouter>
          <div>
            <Route
              exact
              path="/react/college"
              component={props => (
                <Colleges token={this.state.token} {...props} />
              )}
            />
            <Route
              exact
              path="/react/college/:collegeid"
              component={props => (
                <StudentListComponent token={this.state.token} {...props} />
              )}
            />
            <Route
              exact
              path="/react/college/:collegeid/students/:studentid"
              component={props => (
                <StudentDetailComponent token={this.state.token} {...props} />
              )}
            />
            <Route
              exact
              path="/"
              component={props => (
                <Colleges token={this.state.token} {...props} />
              )}
            />
          </div>
        </BrowserRouter>
      </div>
    );
  }
}

export default App;
