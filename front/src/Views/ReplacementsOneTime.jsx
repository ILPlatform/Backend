// src/Views/ReplacementsOneTime.jsx

import React, { useEffect, useState } from "react";
import { Button, Container, Dialog, DialogActions, DialogContent, DialogTitle } from "@mui/material";
import TableComponent from "../Components/ReplacementsOneTime/Table";
import CreatePopup from "../Components/ReplacementsOneTime/CreatePopup";
import { callFunction } from "../firebase";

const ReplacementsOneTime = () => {
  const [replacements, setReplacements] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [classes, setClasses] = useState([]);
  const [openCreate, setOpenCreate] = useState(false);

  useEffect(() => {
    // Fetch one-time replacements
    callFunction("replacements_get_one_time")().then((response) => {
      setReplacements(response?.data?.response);
    });

    // // Fetch teachers
    // callFunction("replacements_get_teachers")().then((response) => {
    //   setTeachers(response.data);
    // });

    // // Fetch classes
    // callFunction("replacements_get_classes")().then((response) => {
    //   setClasses(response.data);
    // });
  }, []);

  const handleCreate = (newReplacement) => {
    setOpenCreate(false);
    // Add the newly created replacement to the table
    setReplacements((prev) => [...prev, newReplacement]);
  };

  return (
    <Container>
      <Button
        variant="contained"
        color="primary"
        onClick={() => setOpenCreate(true)}
        style={{ marginBottom: "20px", float: "right" }}
      >
        New One-Time Replacement
      </Button>

      <TableComponent data={replacements} teachers={teachers} />

      <CreatePopup
        open={openCreate}
        handleClose={() => setOpenCreate(false)}
        handleConfirm={handleCreate}
        classes={classes}
        teachers={teachers}
      />
    </Container>
  );
};

export default ReplacementsOneTime;
