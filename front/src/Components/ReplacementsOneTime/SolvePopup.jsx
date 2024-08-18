// src/Components/ReplacementsOneTime/SolvePopup.jsx

import React, { useState } from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Button,
  TextField,
  List,
  ListItem,
  ListItemText,
  Stepper,
  Step,
  StepLabel,
  DialogContentText,
} from "@mui/material";
import { callFunction } from "../../firebase";

const SolvePopup = ({ open, handleClose, data, teachers }) => {
  const [activeStep, setActiveStep] = useState(0);
  const [selectedTeacher, setSelectedTeacher] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleTeacherSelect = (teacher) => {
    setSelectedTeacher(teacher);
  };

  const handleConfirm = () => {
    // Call the backend API to solve the replacement
    callFunction("replacements_solve")({
      id: data?.id,
      teacher_new: selectedTeacher?.id,
    })
      .then((response) => {
        // Handle the success or failure of the solve operation
        if (response.data.status === "success") {
          alert("Replacement solved successfully.");
        } else {
          alert("Failed to solve replacement.");
        }
        handleClose();
      })
      .catch(() => {
        alert("An error occurred. Please try again.");
        handleClose();
      });
  };

  const filteredTeachers = teachers.filter((teacher) => teacher.name.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Solve Replacement</DialogTitle>
      <DialogContent>
        <Stepper activeStep={activeStep} alternativeLabel>
          <Step>
            <StepLabel>Select New Teacher</StepLabel>
          </Step>
          <Step>
            <StepLabel>Confirm Replacement</StepLabel>
          </Step>
        </Stepper>
        {activeStep === 0 ? (
          <>
            <TextField
              label="Search Teacher"
              fullWidth
              margin="normal"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <List>
              {filteredTeachers.map((teacher) => (
                <ListItem
                  button
                  key={teacher.id}
                  selected={selectedTeacher && selectedTeacher.id === teacher.id}
                  onClick={() => handleTeacherSelect(teacher)}
                >
                  <ListItemText primary={teacher.name} />
                </ListItem>
              ))}
            </List>
          </>
        ) : (
          <>
            <DialogContentText>
              You are about to replace <strong>{data?.teacher_old}</strong> with{" "}
              <strong>{selectedTeacher?.name}</strong>.
            </DialogContentText>
            <List>
              <ListItem>
                <ListItemText primary="Class Code" secondary={data?.code || "N/A"} />
              </ListItem>
              <ListItem>
                <ListItemText primary="School" secondary={data?.school || "N/A"} />
              </ListItem>
              <ListItem>
                <ListItemText primary="Date" secondary={data?.date || "N/A"} />
              </ListItem>
              <ListItem>
                <ListItemText primary="Time" secondary={data?.time || "N/A"} />
              </ListItem>
            </List>
          </>
        )}
      </DialogContent>
      <DialogActions>
        {activeStep === 0 ? (
          <Button onClick={handleClose} color="primary">
            Cancel
          </Button>
        ) : (
          <Button onClick={handleBack} color="primary">
            Back
          </Button>
        )}
        {activeStep === 0 ? (
          <Button onClick={handleNext} color="primary" disabled={!selectedTeacher}>
            Next
          </Button>
        ) : (
          <Button onClick={handleConfirm} color="primary">
            Confirm
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
};

export default SolvePopup;
