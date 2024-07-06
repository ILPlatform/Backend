// React Function Component to Show a number fo Checkboxes
import React from "react";
import GenericForm from "./GenericForm";

const GetTeachersPartners = () => {
  const [data, setData] = React.useState({ partner: "", only_confirmed: false });

  return (
    <GenericForm
      endpoint="admin_get_teachers_partners"
      data={data}
      displayResponse={(res) => (
        <>
          Response: <br />
          {res?.map((teacher) => (
            <>
              {teacher}
              <br />
            </>
          ))}
        </>
      )}
      formChild={
        <>
          {" "}
          <h1>Get Teachers for Partners</h1>
          <div className="textfields">
            <label>
              Partner:
              <input
                type="text"
                value={data.partner}
                onChange={(e) => setData({ ...data, partner: e.target.value })}
                placeholder="Ex: Dynamix23"
              />
            </label>
          </div>
          <div className="checkboxes">
            <label>
              Only Confirmed:
              <input
                type="checkbox"
                checked={data.only_confirmed}
                onChange={() => setData({ ...data, only_confirmed: !data.only_confirmed })}
              />
            </label>
          </div>
        </>
      }
    />
  );
};

export default GetTeachersPartners;
