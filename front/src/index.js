import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router-dom";

// Styles
import "bootstrap/scss/bootstrap.scss";
import "./assets/scss/paper-kit.scss";

// Views
import Login from "./Views/Login";
import Home from "./Views/Home";
import Error from "./Views/404";
import CreateCampsForm from "./Views/CreateCampsForm";
import UpdateCampsEvents from "./Views/UpdateCampsEvents";
import GetTeachersPartners from "./Views/GetTeachersPartners";
import CreateTeacherConvention from "./Views/CreateTeacherConvention";
import CreateTeacherAttestations from "./Views/CreateTeacherAttestations";

// Components
import RequireAuth from "./RequireAuth";
import NavBar from "./Components/Navbar";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <BrowserRouter>
    <RequireAuth exclude={["login"]}>
      <NavBar />
      <div className="p-5 m-5">
        <Routes>
          <Route path="/" exact Component={Home} />
          <Route path="/login" exact Component={Login} />

          <Route path="/create_camps_form" exact Component={CreateCampsForm} />
          <Route path="/update_camps_events" exact Component={UpdateCampsEvents} />
          <Route path="/get_teachers_partners" exact Component={GetTeachersPartners} />
          <Route path="/create_teacher_convention" exact Component={CreateTeacherConvention} />
          <Route path="/create_teacher_attestations" exact Component={CreateTeacherAttestations} />

          <Route path="*" Component={Error} />
        </Routes>
      </div>
    </RequireAuth>
  </BrowserRouter>,
);
