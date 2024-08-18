// src/Components/ReplacementsOneTime/DeletePopup.jsx

import React from "react";
import { Dialog, DialogActions, DialogContent, DialogTitle, Button, List, ListItem, ListItemText } from "@mui/material";
import { callFunction } from "../../firebase";

const DeletePopup = ({ open, handleClose, data }) => {
  const handleConfirm = () => {
    // Call the backend API to delete the replacement
    callFunction("replacements_delete")({ id: data?.id })
      .then((response) => {
        // Handle the success or failure of the deletion
        if (response.data.status === 200) {
          alert("Replacement deleted successfully.");
        } else {
          alert("Failed to delete replacement.");
        }
        handleClose();
      })
      .catch(() => {
        alert("An error occurred. Please try again.");
        handleClose();
      });
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>Confirm Deletion</DialogTitle>
      <DialogContent>
        <List>
          <ListItem>
            <ListItemText primary="Code" secondary={data?.code || "N/A"} />
          </ListItem>
          <ListItem>
            <ListItemText primary="School" secondary={data?.school || "N/A"} />
          </ListItem>
          <ListItem>
            <ListItemText primary="Old Teacher" secondary={data?.teacher_old || "N/A"} />
          </ListItem>
          <ListItem>
            <ListItemText primary="New Teacher" secondary={data?.teacher_new || "N/A"} />
          </ListItem>
          <ListItem>
            <ListItemText primary="Date" secondary={data?.date || "N/A"} />
          </ListItem>
          <ListItem>
            <ListItemText primary="Time" secondary={data?.time || "N/A"} />
          </ListItem>
        </List>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} color="primary">
          Cancel
        </Button>
        <Button onClick={handleConfirm} color="secondary">
          Confirm
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DeletePopup;
