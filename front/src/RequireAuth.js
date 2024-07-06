import { auth } from "./firebase";
import { onAuthStateChanged } from "firebase/auth";
import React, { useState } from "react";
import { Navigate, useLocation } from "react-router-dom";

// TODO: Pass this list to the backend (else it is not secure and can easily be modified)
let ALLOWED_UIDS = ["if4o0vOCGVV62JGgevgQXebtJMI2", "x0YZB7Z0ETUT0HzMscMQ6IrataY2"];

const RequireAuth = ({ children, exclude }) => {
  const [ret, setRet] = useState(<></>);

  const path = useLocation().pathname.split("/")[1];
  onAuthStateChanged(auth, (user) => {
    let allowed = user && ALLOWED_UIDS.includes(user?.uid);
    setRet(!allowed && !exclude?.includes(path) ? <Navigate to="/login" replace /> : children);
  });

  return ret;
};

export default RequireAuth;
