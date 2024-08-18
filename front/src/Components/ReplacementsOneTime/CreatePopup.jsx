// src/Components/ReplacementsOneTime/CreatePopup.jsx

import React, { useState } from "react";
import {
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Button,
  TextField,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  List,
  ListItem,
  ListItemText,
} from "@mui/material";
import { DatePicker } from "@mui/x-date-pickers";
import { callFunction } from "../../firebase";

const CreatePopup = ({ open, handleClose, classes, teachers }) => {
  const [classCode, setClassCode] = useState("");
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTeacher, setSelectedTeacher] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");

  const handleClassCodeChange = (event) => {
    setClassCode(event.target.value);
    setSelectedDate(null);
  };

  const handleDateChange = (date) => {
    setSelectedDate(date);
  };

  const handleTeacherSelect = (teacher) => {
    setSelectedTeacher(teacher);
  };

  const handleConfirm = () => {
    // Call the backend API to create the one-time replacement
    callFunction("replacements_create_one_time")({
      class_code: classCode,
      date: selectedDate,
      teacher_new: selectedTeacher?.id,
    })
      .then((response) => {
        // Handle the success or failure of the create operation
        if (response.data.status === "success") {
          alert("Replacement created successfully.");
        } else {
          alert("Failed to create replacement.");
        }
        handleClose();
      })
      .catch(() => {
        alert("An error occurred. Please try again.");
        handleClose();
      });
  };

  const filteredTeachers = teachers.filter((teacher) => teacher.name.toLowerCase().includes(searchTerm.toLowerCase()));

  const selectedClass = classes.find((cls) => cls.class_code === classCode);

  const disableNonClassDay = (date) => {
    if (!selectedClass) return false;
    const dayOfWeek = date.getDay(); // Sunday = 0, Monday = 1, etc.
    const classDay = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].indexOf(
      selectedClass.class_day,
    );
    return dayOfWeek !== classDay;
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Create One-Time Replacement</DialogTitle>
      <DialogContent>
        <FormControl fullWidth margin="normal">
          <InputLabel id="class-code-label">Class Code</InputLabel>
          <Select labelId="class-code-label" value={classCode} onChange={handleClassCodeChange}>
            {classes.map((cls) => (
              <MenuItem key={cls.class_code} value={cls.class_code}>
                {cls.class_code} - {cls.class_day}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <DatePicker
          label="Select Date"
          value={selectedDate}
          onChange={handleDateChange}
          shouldDisableDate={disableNonClassDay}
          renderInput={(params) => <TextField {...params} fullWidth margin="normal" />}
        />
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
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleConfirm} color="primary">
          Create
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default CreatePopup;
