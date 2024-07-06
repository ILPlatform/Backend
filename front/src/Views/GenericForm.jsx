// React Function Component to Show a number fo Checkboxes
import React from "react";
import { callFunction } from "../firebase";

const GenericForm = ({ formChild, displayResponse, endpoint, data }) => {
  // State variables
  const [loading, setLoading] = React.useState(false);
  const [buttonClicked, setButtonClicked] = React.useState(false);
  const [response, setResponse] = React.useState("");
  const [error, setError] = React.useState("");

  // Async function to update camp events on backend
  const submitForm = async () => {
    try {
      setLoading(true);
      setButtonClicked(true);
      let res = await callFunction(endpoint)(data);
      if (res["data"]["status"] === 200) setResponse(res["data"]["response"]);
      else setError(res["data"]["error"]);
      setLoading(false);
    } catch (error) {
      alert(`Firebase ERROR: ${error.message}. Contact Admin.`);
      setError(error.message);
      setLoading(false);
    }
  };

  return (
    <>
      <fieldset disabled={buttonClicked}>
        {formChild}
        <button onClick={submitForm}>Submit</button>
      </fieldset>
      {loading && buttonClicked ? <div>Loading...</div> : ""}
      {response ? displayResponse(response) : ""}
      {error ? <div>ERROR: {error}. Contact Admin.</div> : ""}
    </>
  );
};

export default GenericForm;
