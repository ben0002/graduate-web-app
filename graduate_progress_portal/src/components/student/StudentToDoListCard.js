import React, { useEffect, useState } from 'react';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { DatePicker } from '@mui/x-date-pickers';

function ToDoModal(task, openModal, closeModal, methods, newTask){
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(_ => {
    setIsNew(newTask);
    setEdit(newTask);
  }, [newTask])

  /*
  useEffect(_ => {
    async function newEvent(){
      await fetch("https://bktp-gradpro-api.discovery.cs.vt.edu/student/course/4", {
          method: 'DELETE',
          credentials: 'include', // To include cookies in the request
          headers: {
              'Accept': 'application/json', // Explicitly tell the server that you want JSON
              'Content-Type': 'application/json',
          },
          
      })
      .then(res => {
          if(res.ok) return res.json();
          else console.log(res.status);
      })
      .then(data => {
          if (data == undefined) console.error('Error: Non ok http response');
          else{
              console.log(data)
          }
      })
      .catch((err) => console.error('Error:', err.message))
    }
    newEvent()
  }, [])
  */

  const checkChanged = _ => {
    return true
  }

  const checkNewFields = save => {
    var valid = true
    if(save && valid) setIsNew(false)
    return valid
  }

  if(task == null && !isNew) {return(<></>)}

  return(
    <Modal open={openModal || isNew} onClose={_ => {closeModal(); setEdit(false)}}>
      <Box style={{width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
        <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
          {edit ? <TextField/> : <h1 style={{margin: '0'}}>{task ? task.Name : ''}</h1>}
          <div style={{display: 'flex'}}>
            <IconButton onClick={_ => (isNew ? checkNewFields(false) ? setConfirmDelete(true) : closeModal() : setEdit(!edit))}>
              <EditIcon sx={{color: '#630031'}}/>
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <HighlightOffIcon sx={{color: '#630031'}}/>
            </IconButton>
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingRight: '.75rem'}}>
          <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}> <b style={{marginRight: '0.25rem'}}>Start Date:</b> {edit ? <DatePicker/> : 'mm/dd/yyyy'}</Typography>
          <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}> <b style={{marginRight: '0.25rem'}}>End/Due Date:</b> {edit ? <DatePicker/> : 'mm/dd/yyyy'}</Typography>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch disabled={!edit}/>
            <Typography> Completed </Typography>
          </div>
        </div>
        <h3 style={{margin: '0.25rem 0'}}>Description:</h3>
        {edit ? 
          <textarea style={{resize: 'none', height: '15rem', width: 'calc(100% - 0.5rem)'}}/>
          : 
          <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '15rem'}}>
            <Typography>Placeholder text</Typography>
          </div> 
        }
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
        {edit ? <Button style={{position: 'absolute', right: '1rem', bottom: '1rem'}} variant='outlined' onClick={_ => (isNew ? checkNewFields(true) : setEdit(false))} disabled={checkChanged()}>Save</Button> : <></>}
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)}>
          <Box style={{width: '13.5%', backgroundColor: 'white', margin: '12.5% auto', padding: '1rem', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <h2 style={{marginTop: '0'}}>Are you sure you want to delete this event?</h2>
            <Button variant='outlined' style={{marginRight: '1rem'}} onClick={_ => {if(!isNew){methods.removeTask(task.id)} setConfirmDelete(false); closeModal(); setEdit(false)}}>Confrim</Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>Keep Event</Button>
          </Box>
        </Modal>
      </Box>
    </Modal>
  )
}

export default function  ToDoList() {

  const [tasks, setTasks] = useState([{Name: "First", id: 1, description: 'Placeholder text'}]);
  const [makeNew, setMakeNew] = useState(false);
  const [modal, setModal] = useState(null);

  var closeModal = _ => {
    setModal(null)
    setMakeNew(false)
  }

  var addTask = newTask => {
    setTasks(tasks.concat(newTask))
    setMakeNew(false)
  }

  var removeTask = id => {
    setTasks(tasks.filter( task => task.id !== id))
  }

  var makeTaskCards = _ => {
    return tasks.map( (task, idx) => { return(
      <Card raised sx={{marginX: '0.5rem'}} onClick={ _ => {setModal(task); setMakeNew(false)}} key={`task-${idx}`}>
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
    <Card className="to-do-list-container" sx={{backgroundColor: '#F0F0F0'}}>
      <CardContent sx={{ padding: '8px 16px'}}>
        <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
          <strong>To Do List</strong>
          <IconButton onClick={ _ => setMakeNew(true)}>
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
    {ToDoModal(modal, modal !== null, closeModal, {removeTask, addTask}, makeNew)}
    </>
  );
}
