import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import './StudentToDoListCard.css';

const ToDoList = () => {
  return (
    <Card className="to-do-list-container">
      <CardContent sx={{ padding: '8px 16px'}}>
        <Typography variant="h6" component="div">
          <strong>To Do List</strong>
        </Typography>
        {/* Placeholder box, uses the to-do-list-placeholder class for styling */}
        <div className="to-do-list-placeholder">
          <Typography variant="body1">No tasks yet</Typography>
        </div>
      </CardContent>
    </Card>
  );
}

export default ToDoList;
