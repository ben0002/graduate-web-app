import React, { useState, useEffect } from 'react';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { DatePicker } from '@mui/x-date-pickers';

function EmploymentModal(employment, openModal, closeModal, methods, newEmployment){
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  useEffect(_ => {
    setIsNew(newEmployment);
    setEdit(newEmployment);
  }, [newEmployment])

  const checkChanged = _ => {
    return true
  }

  const checkNewFields = save => {
    var valid = true
    if(save && valid) setIsNew(false)
    return valid
  }

  if(employment == null && !isNew) {return(<></>)}
  
    return(
      <Modal open={openModal || isNew} onClose={_ => {closeModal(null); setEdit(false)}}>
      <Box style={{width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
         {edit ? <div><TextField/> <b style={{fontSize: '2rem'}}>-</b> <TextField/></div>: <h1 style={{margin: '0'}}>Company - Title</h1>}
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
          <div style={{display: 'flex', flexDirection: 'column', alignItems: `${edit ? 'end' : 'start'}`, justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <p style={{margin: '0', display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Salary:</b> {edit ? <TextField/> : '$$$$$'}</p>
            <p style={{margin: '0', display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Employment Type:</b> {edit ? <TextField/> : 'Type'}</p>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'end', justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Employment Start:</b> {edit ? <DatePicker/> : 'mm/dd/yyyy'}</Typography>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Employment End:</b> {edit ? <DatePicker/> : 'mm/dd/yyyy'}</Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch disabled={!edit}/>
            <Typography> Accepted </Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch disabled={!edit}/>
            <Typography> Gauranteed </Typography>
          </div>
        </div>
        {/* POSSIBLY CONVERT TO TABS */}
        <h3 style={{margin: '0.25rem 0'}}>Description:</h3>
        <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '6.5rem'}}>
          <Typography>Placeholder text</Typography>
        </div>
        <h3 style={{margin: '0.25rem 0'}}>Notes:</h3>
        {edit ? 
          <textarea style={{resize: 'none', height: '7rem', width: 'calc(100% - 0.5rem)'}}/>
          :
          <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '7rem'}}>
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
            <Button variant='outlined' style={{marginRight: '1rem'}} onClick={_ => {if(!isNew){methods.removeEmployment(employment.id)} setConfirmDelete(false); closeModal(null); setEdit(false)}}>Confrim</Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>Keep Event</Button>
          </Box>
        </Modal>
      </Box>
    </Modal>
  )
}

export default function StudentEmploymentCard() {

  const [employments, setEmployments] = useState([{Name: "First", id: 1}]);
  const [makeNew, setMakeNew] = useState(false);
  const [modal, setModal] = useState(null);

  var closeModal = _ => {
    setModal(null)
    setMakeNew(false)
  }
  
  var addEmployment = newEmployment => {
    setEmployments(employments.concat(newEmployment))
    setMakeNew(false)
  }

  var removeEmployment = id => {
    setEmployments(employments.filter( employment => employment.id != id))
  }

  var makeEmploymentCards = _ => {
    return employments.map( employment => { return(
      <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', borderBottom: '1px solid lightgray'}} onClick={_ => {setModal(employment); setMakeNew(false)}}>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between'}}>
          <h2 style={{margin: '0'}}>{employment.Name}</h2>
          <p style={{margin: '0'}}>$$$$$</p>
        </div>
        <div>
          <p style={{margin: '0', fontSize: '0.75rem', display: 'inline-block'}}>sept. 20, 2020 -</p>
          <p style={{margin: '0', fontSize: '0.75rem', display: 'inline-block'}}>sept. 31, 2020</p>
        </div>
      </div>
    )})
  }

  return (
    <>
    <Card className="student-employment-card-container">
      <CardContent>
        <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
          <strong>Student Employment</strong>
          <IconButton onClick={ _ => setMakeNew(false)}>
            <AddCircleOutlineIcon sx={{color: '#630031'}}/>
          </IconButton>
        </Typography>
        <div style={{overflowY: 'scroll', overflowX: 'hidden', minHeight: '16.25rem', maxHeight: '16.25rem'}}>
          <div className="student-employment-card-placeholder">
            {makeEmploymentCards()}
          </div>
        </div>
      </CardContent>
    </Card>
    {EmploymentModal(modal, modal !== null, closeModal, {removeEmployment, addEmployment}, makeNew)}
    </>
  );
};
