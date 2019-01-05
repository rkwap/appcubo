import React, { Component } from 'react';
import logo from './logo.svg';
import axios from 'axios';
import './App.css';
const API = '/apps/android/search/subway';


class App extends Component{
  constructor(){
  super();
  this.state={
     results: [],
     isLoading: false,
     error: null,
   }
}

componentDidMount(){
  this.setState({
     isLoading: true
    })
  fetch(API)
  .then(response => {
       if(response.ok){
       return response.json()
      }else{
      throw new Error('Something went wrong...')
    }
 })
  .then(data => this.setState({
    results: data.results,
    isLoading: false
  }))
  .catch(error => this.setState({
     error: null, 
     isLoading: false
  }))
 }

render(){
const {results, isLoading, error} = this.state;

    if(isLoading){
      return <p>Please Wait. Loading...</p>
    }
    if(error){
      return <p>{error.message}</p>
     }
return(
    <div className="container">

        {results.map(data => 
          <ul key={data.id}>
            <img src={data.icon} width="100"></img>   
            <li><a href={data.appURL}>Title:  {!!data.title ? data.title : "Not Available" }</a></li>
            <li>Publisher:{data.publisher}</li>
            <li>appID: {data.appID}</li>
          </ul> 
        )}
    </div>
   )
  }
}
export default App
