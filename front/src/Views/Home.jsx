import React from "react";

const Home = () => {
  return (
    <>
      <h1>Home</h1>
      <a href="/create_camps_form">Create Camps Form (Deprecated, on Salesforce)</a>
      <br />
      <a href="/update_camps_events">Update Camps Events (Deprecated, on Salesforce)</a>
      <br />
      <a href="/update_classes_events">Update Classes Events</a>
      <br />
      <a href="/get_teachers_partners">Get Teachers for Partners</a>
      <br />
      <a href="/create_teacher_convention">Get Teacher Convention</a>
      <br />
      <a href="/create_teacher_attestations">Get Teacher Attestations</a>
    </>
  );
};

export default Home;
