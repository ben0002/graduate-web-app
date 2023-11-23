import React, { useState } from 'react';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
//import './ToDoBox.css';

var count = 2;

function ToDoModal(task, openModal, closeModal, removeTask){
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  if(task == null) return(<></>)

  return(
    <Modal open={openModal} onClose={_ => closeModal(null)}>
      <Box style={{width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
        <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
          <h1 style={{margin: '0'}}>{task.Name}</h1>
          <div style={{display: 'flex'}}>
            <IconButton onClick={_ => removeTask(task.id)}>
              <EditIcon sx={{color: '#630031'}}/>
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <HighlightOffIcon sx={{color: '#630031'}}/>
            </IconButton>
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingRight: '.75rem'}}>
          <Typography> <b>Start Date:</b> mm/dd/yyyy</Typography>
          <Typography> <b>End/Due Date:</b> mm/dd/yyyy</Typography>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch/>
            <Typography> Completed </Typography>
          </div>
        </div>
        <h3 style={{margin: '0.25rem 0'}}>Description:</h3>
        <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '15rem'}}>
          <Typography>Placeholder text</Typography>
        </div>
        <div style={{position: 'absolute', left: '1rem', bottom: '1rem'}}>
          <div style={{display: 'flex', alignItems: 'center'}}>
            <h3 style={{display: 'inline-block', margin: '0.5rem 0'}}> Files: </h3>
            <Button component='label' startIcon={<FileUploadIcon sx={{color: '#630031'}}/>}>
              <Input type='file' style={{width: '0'}} onChange={ e => console.log(e.target.files)}/>
            </Button>
          </div>
          <div style={{height: '2rem', width: 'fit-content', border: '1px solid lightgray', borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 1rem'}}>
            <h3 style={{margin: '0'}}>File1.pdf</h3>
          </div>
        </div>
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)}>
          <Box style={{width: '13.5%', backgroundColor: 'white', margin: '12.5% auto', padding: '1rem', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <h2 style={{marginTop: '0'}}>Are you sure you want to delete this event?</h2>
            <Button variant='outlined' style={{marginRight: '1rem'}} onClick={_ => {removeTask(task.id); setConfirmDelete(false); closeModal(null)}}>Confrim</Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>Keep Event</Button>
          </Box>
        </Modal>
      </Box>
    </Modal>
  )
}

export default function  ToDoList() {

  const [tasks, setTasks] = useState([{Name: "First", id: 1, description: 'Placeholder text'}]);
  const [modal, setModal] = useState(null);

  var addTask = _ => {
    setTasks(tasks.concat({Name: `${count}`, id: count}))
    count += 1;
  }

  var removeTask = id => {
    setTasks(tasks.filter( task => task.id !== id))
  }

  var makeTaskCards = _ => {
    return tasks.map( task => { return(
      <Card raised sx={{marginX: '0.5rem'}} onClick={ _ => setModal(task)}>
        <CardContent style={{display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'left', width: '10rem', height: '10rem', paddingBottom: '1.5rem'}}>
          <h1 style={{margin: '0'}}>{task.Name}</h1>
          <p>{task.description}</p>
          <p style={{marginBottom: '0'}}><b>Due:</b> mm/dd/yyyy</p>
        </CardContent>
      </Card>
    )
    })
  }

  return (
    <>
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
    {ToDoModal(modal, modal !== null, setModal, removeTask)}
    </>
  );
}
