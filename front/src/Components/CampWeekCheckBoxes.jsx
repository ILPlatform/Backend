import React from "react";
import { callFunction } from "../firebase";
import { useEffect } from "react";

const CampWeekCheckBoxes = ({ checked, setChecked }) => {
  const [error, setError] = React.useState("");
  const [authError, setAuthError] = React.useState("");
  const [weekCodes, setWeekCodes] = React.useState([]);
  const [loadingWeekCodes, setLoadingWeekCodes] = React.useState(false);

  // Async function to get week codes
  useEffect(() => {
    const getWeekCodes = async () => {
      try {
        let res = await callFunction("admin_get_week_codes")({});
        if (res["data"]["status"] === 200) setWeekCodes(res["data"]["response"]);
        else setAuthError(res["data"]["error"]);
        setLoadingWeekCodes(true);
      } catch (error) {
        setError(`Firebase ERROR: ${error.message}`);
      }
    };
    getWeekCodes();
  }, []);

  // Function to update checked items
  const updateChecked = (item) => {
    if (checked.includes(item)) setChecked(checked.filter((i) => i !== item));
    else setChecked([...checked, item]);
  };

  if (error) return error;

  return loadingWeekCodes ? (
    authError ? (
      authError
    ) : (
      <>
        <p>Week Codes:</p>
        <div className="checkboxes">
          {weekCodes?.map(({ code, name }, index) => (
            <div key={index} className="checkbox">
              <label>
                <input type="checkbox" checked={checked.includes(code)} onChange={() => updateChecked(code)} />
                {name}
              </label>
            </div>
          ))}
        </div>
      </>
    )
  ) : (
    "Loading Week Codes..."
  );
};

export default CampWeekCheckBoxes;
