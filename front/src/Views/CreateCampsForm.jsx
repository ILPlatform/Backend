// React Function Component to Show a number fo Checkboxes
// Path: GenerateCheckboxes.jsx

import React from "react";
import CampWeekCheckBoxes from "../Components/CampWeekCheckBoxes";
import GenericForm from "./GenericForm";

const CreateCampsForm = () => {
  // State variables
  const [data, setData] = React.useState({ title: "", week_codes: [] });

  return (
    <GenericForm
      endpoint="admin_create_camps_form"
      data={{ title: `ILPlatform Stages ${data.title}`, week_codes: data.week_codes.sort() }}
      displayResponse={(res) => (
        <>
          Response: <a href={res}> {res}</a>
        </>
      )}
      formChild={
        <>
          <h1>Create Camps Form</h1>
          <div className="textfields">
            <label>
              Form Period:
              <input
                type="text"
                value={data.title}
                onChange={(e) => setData({ ...data, title: e.target.value })}
                placeholder="Ex: Août 2024"
              />
            </label>
          </div>
          <CampWeekCheckBoxes
            checked={data.week_codes}
            setChecked={(checked) => setData({ ...data, week_codes: checked })}
          />
        </>
      }
    />
  );
};

export default CreateCampsForm;
