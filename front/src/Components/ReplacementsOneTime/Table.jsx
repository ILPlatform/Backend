// src/Components/ReplacementsOneTime/Table.jsx

import React, { useState, useMemo } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
} from "@mui/material";
import DeletePopup from "./DeletePopup";
import SolvePopup from "./SolvePopup";

const TableComponent = ({ data, teachers, onDelete, onSolve, filters }) => {
  const [orderBy, setOrderBy] = useState("created_timestamp");
  const [order, setOrder] = useState("asc");
  const [filter, setFilter] = useState("All");
  const [selectedRow, setSelectedRow] = useState(null);
  const [openDelete, setOpenDelete] = useState(false);
  const [openSolve, setOpenSolve] = useState(false);

  const columns = {
    created_timestamp: "Created Timestamp",
    code: "Class Code",
    day: "Day",
    date: "Class Date",
    time: "Class Time",
    teacher_old: "Old Teacher",
    teacher_new: "New Teacher",
  };

  const handleRequestSort = (property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const filteredData = useMemo(() => {
    switch (filter) {
      case "Past":
        return data.filter((item) => new Date(item.date) < new Date());
      case "Future":
        return data.filter((item) => new Date(item.date) >= new Date());
      case "Unresolved":
        return data.filter((item) => !item.teacher_new);
      default:
        return data;
    }
  }, [data, filter]);

  const sortedData = useMemo(() => {
    return filteredData.sort((a, b) => {
      if (order === "asc") {
        return a[orderBy] < b[orderBy] ? -1 : 1;
      } else {
        return a[orderBy] > b[orderBy] ? -1 : 1;
      }
    });
  }, [filteredData, order, orderBy]);

  const handleDelete = (row) => {
    setSelectedRow(row);
    setOpenDelete(true);
  };

  const handleSolve = (row) => {
    setSelectedRow(row);
    setOpenSolve(true);
  };

  return (
    <div>
      <FormControl variant="outlined" style={{ minWidth: 120, marginBottom: "16px" }}>
        <InputLabel>Filter</InputLabel>
        <Select value={filter} onChange={(e) => setFilter(e.target.value)} label="Filter">
          <MenuItem value="All">All</MenuItem>
          <MenuItem value="Past">Past</MenuItem>
          <MenuItem value="Future">Future</MenuItem>
          <MenuItem value="Unresolved">Unresolved</MenuItem>
        </Select>
      </FormControl>

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              {Object.keys(columns).map((columnKey) => (
                <TableCell key={columnKey}>
                  <TableSortLabel
                    active={orderBy === columnKey}
                    direction={orderBy === columnKey ? order : "asc"}
                    onClick={() => handleRequestSort(columnKey)}
                  >
                    {columns[columnKey]}
                  </TableSortLabel>
                </TableCell>
              ))}
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {sortedData.map((row) => (
              <TableRow key={row?.id}>
                {Object.keys(columns).map((columnKey) => (
                  <TableCell key={columnKey}>{row?.[columnKey]}</TableCell>
                ))}
                <TableCell>
                  <Button color="primary" onClick={() => handleSolve(row)}>
                    Solve
                  </Button>
                  <Button color="secondary" onClick={() => handleDelete(row)}>
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <DeletePopup open={openDelete} handleClose={() => setOpenDelete(false)} data={selectedRow} />

      <SolvePopup open={openSolve} handleClose={() => setOpenSolve(false)} data={selectedRow} teachers={teachers} />
    </div>
  );
};

export default TableComponent;
