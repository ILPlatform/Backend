// React Function Component to Show a number fo Checkboxes
import React from "react";

// Import Components
import CampWeekCheckBoxes from "../Components/CampWeekCheckBoxes";
import GenericForm from "./GenericForm";

const UpdateCampEvents = () => {
  const [data, setData] = React.useState({ week_codes: [] });

  return (
    <GenericForm
      endpoint="admin_update_camps_events"
      data={{ week_codes: data.week_codes.sort() }}
      displayResponse={(res) => <>{res}</>}
      formChild={
        <>
          <h1>Update Camps Events</h1>
          <CampWeekCheckBoxes
            checked={data.week_codes}
            setChecked={(checked) => setData({ ...data, week_codes: checked })}
          />
        </>
      }
    />
  );
};

export default UpdateCampEvents;
