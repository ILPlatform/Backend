// React Function Component to Show a number fo Checkboxes
import React from "react";
import GenericForm from "./GenericForm";

const CreateTeacherConvention = () => {
  const [data, setData] = React.useState({ email: "" });

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
        </>
      }
    />
  );
};

export default CreateTeacherConvention;
