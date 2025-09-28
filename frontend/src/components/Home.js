import React, { useEffect, useState } from "react";
import axios from "axios";
const API_BASE_URL_HELLO = process.env.REACT_APP_API_BASE_URL_HELLO;
const API_BASE_URL_PROFILE = process.env.REACT_APP_API_BASE_URL_PROFILE;

function Home() {
  const [message, setMessage] = useState("");
  const [profile, setProfile] = useState([]);

  useEffect(() => {
    axios
      .get(API_BASE_URL_HELLO)
      .then((response) => {
        setMessage(response.data.msg);
      })
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  useEffect(() => {
    axios
      .get(`${API_BASE_URL_PROFILE}/user/fetch`)
      .then((response) => {
        setProfile(response.data);
        
      })
      .catch((error) => console.error("Error fetching data:", error));
  },[]);

  

  return (
    <div className="App">
      <h1>{message}</h1>
      <div>
        <h2>Profile</h2>
        {
        profile.map((user) => {
            console.log('user', user)
          return (
            <div>
              <h3>Name: {user.name}</h3>
              <h3>Age: {user.age}</h3>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default Home;
