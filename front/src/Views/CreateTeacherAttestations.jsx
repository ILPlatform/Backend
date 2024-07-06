// React Function Component to Show a number fo Checkboxes
import React from "react";
import GenericForm from "./GenericForm";

const CreateTeacherAttestations = () => {
  const [data, setData] = React.useState({ year: "", month: "", name: "" });

  return (
    <GenericForm
      endpoint="admin_create_teacher_attestations"
      data={{ year: parseInt(data.year), month: parseInt(data.month), name: data.name, require_confirm: true }}
      displayResponse={(res) => (
        <div style={{ whiteSpace: "pre-wrap" }}>
          {" "}
          {res.map((r) => (
            <>
              {r}
              <br />
            </>
          ))}
          <GenericForm
            endpoint="admin_create_teacher_attestations"
            data={{ year: parseInt(data.year), month: parseInt(data.month), name: data.name }}
            displayResponse={(res) => <div style={{ whiteSpace: "pre-wrap" }}> {res}</div>}
            formChild={<> </>}
          />
        </div>
      )}
      formChild={
        <>
          <h1>Get Convention for Teachers</h1>
          <div className="textfields">
            <label>
              Year:{" "}
              <input
                type="text"
                value={data.year}
                onChange={(e) => setData({ ...data, year: e.target.value })}
                placeholder="Ex: 2024"
              />
            </label>
            <label>
              Month:{" "}
              <input
                type="text"
                value={data.month}
                onChange={(e) => setData({ ...data, month: e.target.value })}
                placeholder="Ex: 6"
              />
            </label>
            <label>
              Name (If empty, everyone):{" "}
              <input
                type="text"
                value={data.name}
                onChange={(e) => setData({ ...data, name: e.target.value })}
                placeholder="Ex: Test Teacher"
              />
            </label>
          </div>
        </>
      }
    />
  );
};

export default CreateTeacherAttestations;
