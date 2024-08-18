import { auth, callFunction } from "./firebase";
import { onAuthStateChanged } from "firebase/auth";
import React, { useState, useEffect } from "react";
import { Navigate, useLocation } from "react-router-dom";

// TODO: Pass this list to the backend (else it is not secure and can easily be modified)
let ALLOWED_UIDS = ["if4o0vOCGVV62JGgevgQXebtJMI2", "x0YZB7Z0ETUT0HzMscMQ6IrataY2"];

const RequireAuth = ({ children, exclude }) => {
  const [ret, setRet] = useState(<></>);
  const [authorized, setAuthorized] = useState(true);

  useEffect(() => {
    callFunction("curriculum_get_user")().then((result) => {
      console.log(result);
      if (result?.data?.status === 200) {
        setAuthorized(true);
      } else {
        setAuthorized(false);
      }
    });
  }, []);

  const path = useLocation().pathname.split("/")[1];
  onAuthStateChanged(auth, (user) => {
    let allowed = user && ALLOWED_UIDS.includes(user?.uid);
    if (!allowed && !exclude?.includes(path)) {
      setRet(<Navigate to="/login" replace />);
    } else if (!authorized && !exclude?.includes(path)) {
      setRet(
        "Not authorized. We might have a different email on record than the one you are logged in with. Please contact the administrator for more details.",
      );
    } else {
      setRet(children);
    }
  });

  return ret;
};

export default RequireAuth;
