import React, { useState, useEffect } from 'react';
import axios from 'axios';

import Results from './components/Results';
import NewName from './components/NewName';

import logo from './logo.svg';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [names, setNames] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getNames();
  }, [])

  const changeName = (event) => {
    setName(event.target.value);
  }

  const getNames = async() => {
    setLoading(true)
    await axios.get(`/getnames`)
    .then(response => response.json())
    .then(response => {
      console.log(response.data.name)
      setNames(response.data);
    })
    .catch(err => {
      // console.log(err);
    })
  }

  const submitName = async(event) => {
    event.preventDefault();
    setLoading(true);
    await axios.get(`/addname/${name}`)
    .then(response => {
      console.log(response.data)
      setLoading(false);
      setNames(response.data);
    })
    .catch(err => {
      // console.log(err);
    })
  }

  return (
    <div className="App">
      <header className="App-header">
        <NewName handleChange={changeName} handleSubmit={submitName} value={name} />
        {
          loading ? (
            <h1>Loading</h1> 
          ) : (
            <Results name={name} names={names} loading={loading} />
          )
        }
      </header>
    </div>
  );
}

export default App;
