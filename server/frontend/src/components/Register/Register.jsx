import React, { useState } from "react";
import "./Register.css";
import user_icon from "../assets/person.png";
import email_icon from "../assets/email.png";
import password_icon from "../assets/password.png";
import close_icon from "../assets/close.png";

const Register = () => {
  // State variables for form inputs 
  const [userName, setUserName] = useState(""); 
  const [password, setPassword] = useState(""); 
  const [email, setEmail] = useState(""); 
  const [firstName, setFirstName] = useState(""); 
  const [lastName, setLastName] = useState("");

  // Redirect to home 
  const gohome = () => { 
    window.location.href = window.location.origin; 
  };

  // Handle form submission 
  const register = async (e) => { 
    e.preventDefault(); 
    let register_url = window.location.origin + "/djangoapp/register";

    // Send POST request to register endpoint 
    const res = await fetch(register_url, { 
      method: "POST", 
      headers: { 
        "Content-Type": "application/json", 
      }, 
      body: JSON.stringify({ 
        "userName": userName, 
        "password": password,
        "email": email,
        "firstName": firstName,
        "lastName": lastName
      }), 
    });

    const data = await res.json();
    if (res.status === 201) {
      alert("Registration successful!");
      gohome();
    } else {
      alert("Registration failed: " + (data.error || "Unknown error"));
    }
  };

  return (
    <div className="register-container">
      <form onSubmit={register}>
        <h2>Register</h2>

        <label>
          Username:
          <input type="text" value={userName} onChange={(e) => setUserName(e.target.value)} required />
        </label>

        <label>
          Password:
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </label>

        <label>
          Email:
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>

        <label>
          First Name:
          <input type="text" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
        </label>

        <label>
          Last Name:
          <input type="text" value={lastName} onChange={(e) => setLastName(e.target.value)} />
        </label>

        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;

