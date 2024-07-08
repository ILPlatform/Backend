// React Function Component to Show a number fo Checkboxes
import React from "react";
import GenericForm from "./GenericForm";

const CreateTeacherConvention = () => {
  const [data, setData] = React.useState({ email: "", contract: false, end_date: "" });

  return (
    <GenericForm
      endpoint="admin_create_teacher_convention"
      data={data}
      displayResponse={(res) => <a href={res}>{res}</a>}
      formChild={
        <>
          <h1>Get Convention for Teachers</h1>
          <div className="textfields">
            <label>
              Teacher Email:{" "}
              <input
                type="text"
                value={data.email}
                onChange={(e) => setData({ ...data, email: e.target.value })}
                placeholder="Ex: test@ilplatform.be"
              />
            </label>
          </div>
          <div className="selectfields">
            <label>
              Type:{" "}
              <select onChange={(e) => setData({ ...data, contract: e.target.value })}>
                <option value="false">Convention</option>
                <option value="true">Contract</option>
              </select>
            </label>
          </div>
          {data.contract === "true" ? (
            <div className="textfields">
              <label>
                End Date:{" "}
                <input
                  type="text"
                  value={data.end_date}
                  onChange={(e) => setData({ ...data, end_date: e.target.value })}
                  placeholder="Ex: 2024-08-31"
                />
              </label>
            </div>
          ) : (
            ""
          )}
        </>
      }
    />
  );
};

export default CreateTeacherConvention;
