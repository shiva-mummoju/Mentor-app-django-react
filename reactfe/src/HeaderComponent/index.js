import React, { Component } from 'react';



class HeaderComponent extends Component{
    state = {
        loginStatus: false,
    }
    
    toggleLoginStatus = () => {
        this.setState(prev => ({ loginStatus : !prev.loginStatus })  )
    }

    render(){
        let inner;
        if(this.state.loginStatus === true){
            inner = <li><button className="btn btn-primary" onClick = {this.toggleLoginStatus}>Log out</button></li>
        }else{
            inner = <li  ><button className="btn btn-info" onClick = {this.toggleLoginStatus}  >Log in</button></li>
        }
        return (
        <nav className="navbar">
            <a className="navbar-brand">
                Mentor App
            </a>
            <ul className="nav navbar-nav ml-auto" >
                {inner}  
            </ul>
        </nav>
        )}
}


export default HeaderComponent;