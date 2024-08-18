// React Function Component to Show a number fo Checkboxes
import React from "react";

// Import Components
import GenericForm from "./GenericForm";

const UpdateClassesEvents = () => {
  const [data, setData] = React.useState({ class_code: 4 });

  return (
    <>
      <GenericForm
        endpoint="admin_update_single_class_events"
        data={{ class_code: data?.class_code }}
        displayResponse={(res) => <>{res}</>}
        formChild={
          <>
            <h1>Update Classes Events</h1>
            <input
              type="text"
              value={data?.class_code}
              onChange={(e) => setData({ ...data, class_code: e.target.value })}
              placeholder="Class Code"
            />
          </>
        }
      />
      <GenericForm
        endpoint="replacements_create_one_time"
        data={data}
        displayResponse={(res) => <>{res}</>}
        formChild={
          <>
            <h1>Update Classes Events</h1>
            <input
              type="text"
              value={data?.class_code}
              onChange={(e) => setData({ ...data, class_code: e.target.value })}
              placeholder="Class Code"
            />
            <input
              type="date"
              value={data?.date}
              onChange={(e) => setData({ ...data, date: e.target.value })}
              placeholder="Replacement Date"
            />
          </>
        }
      />
    </>
  );
};

export default UpdateClassesEvents;
