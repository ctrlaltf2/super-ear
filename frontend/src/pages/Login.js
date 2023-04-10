import React, { useState } from "react";
import ReactDOM from "react-dom";

function App() {
  // React States
  const [uname, setUname] = useState();
  const [pass, setPass] = useState();
  const [errorMessages, setErrorMessages] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  // User Login info
  const database = [
    {
      username: "user1",
      password: "pass1"
    },
    {
      username: "user2",
      password: "pass2"
    }
  ];

  const errors = {
    uname: "invalid username",
    pass: "invalid password"
  };

  const handleSubmit = (event) => {
    console.log("sub");
    console.log(uname);
    console.log(password);
    //Prevent page reload
    event.preventDefault();
    // Find user login info
    const userData = database.find((user) => user.username === uname);

    // Compare user info
    if (userData) {
      if (userData.password !== pass) {
        // Invalid password
        setErrorMessages({ name: "pass", message: errors.pass });
      } else {
        setIsSubmitted(true);
      }
    } else {
      // Username not found
      setErrorMessages({ name: "uname", message: errors.uname });
    }
  };

  // Generate JSX code for error message
  const renderErrorMessage = (name) =>
    name === errorMessages.name && (
      <div className="error">{errorMessages.message}</div>
    );

  if (isSubmitted){
      return(
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col items-center justify-center">
        <div>
          Login Successful!
        </div>
      </div>);
    }
    else{
    return (
      <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4 flex flex-col">
        <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block text-grey-darker text-sm font-bold mb-2">
            Username
          </label>
          <input className="shadow appearance-none border rounded w-full py-2 px-3 text-grey-darker" 
            onChange={e => setUname(e.target.value)}
            type="text" 
            placeholder="Username" 
            required/>
          {renderErrorMessage("uname")}
        </div>
        <div className="mb-6">
          <label className="block text-grey-darker text-sm font-bold mb-2">
            Password
          </label>
          <input className="shadow appearance-none border border-red rounded w-full py-2 px-3 text-grey-darker mb-3" 
            onChange={e => setPass(e.target.value)}
            type="password" 
            placeholder="******************" 
            required/>
          {renderErrorMessage("pass")}
        </div>
        <div className="flex items-center justify-between">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" type="submit">
              Sign In
          </button>
        </div>
        </form>
      </div>
    );}

}

export default App;