import React, { useState } from 'react';
import { Card, CardContent, IconButton, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
//import './ToDoBox.css';

var count = 2;

export default function  ToDoList() {

  const [tasks, setTasks] = useState([{Name: "First", id: 1}]);

  var addTask = _ => {
    setTasks(tasks.concat({Name: `${count}`, id: count}))
    count += 1;
  }

  var removeTask = id => {
    setTasks(tasks.filter( task => task.id != id))
  }

  var makeTaskCards = _ => {
    return tasks.map( task => { return(
      <Card raised sx={{marginX: '0.5rem'}}>
        <CardContent sx={{display: 'flex', justifyContent: 'center', alignItems: 'center', width: '10rem', height: '10rem', position: 'relative'}}>
          <h1 style={{margin: '0'}}>{task.Name}</h1>
          <IconButton sx={{position: 'absolute', right: '0.5rem', top: '0.5rem'}} onClick={_ => removeTask(task.id)}>
            <HighlightOffIcon sx={{color: '#630031'}}/>
          </IconButton>
        </CardContent>
      </Card>
    )
    })
  }

  return (
    <Card className="to-do-list-container">
      <CardContent sx={{ padding: '8px 16px'}}>
        <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
          <strong>To Do List</strong>
          <IconButton onClick={ _ => addTask()}>
            <AddCircleOutlineIcon sx={{color: '#630031'}}/>
          </IconButton>
        </Typography>
        {/* Placeholder box, uses the to-do-list-placeholder class for styling */}
        <div style={{overflowX: 'scroll'}}>
          <div className="to-do-list-placeholder">
            {makeTaskCards()}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
