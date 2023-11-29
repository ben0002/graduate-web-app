import React, { useState, useEffect } from 'react';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, Tab, Tabs, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import { DatePicker } from '@mui/x-date-pickers';

function MilestoneModal(milestone, openModal, closeModal, methods, newMilestone){
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [tab, setTab] = useState(0);

  useEffect(_ => {
    setIsNew(newMilestone);
    setEdit(newMilestone);
  }, [newMilestone])

  const checkChanged = _ => {
    return true
  }

  const checkNewFields = save => {
    var valid = true
    if(save && valid) setIsNew(false)
    return valid
  }

  const handleTabChange = (_, newTab) => {
    setTab(newTab);
  };

  if(milestone == null && !isNew) {return(<></>)}
  
    return(
      <Modal open={openModal || isNew} onClose={_ => {closeModal(null); setEdit(false)}}>
        <Box style={{width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
          <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
            {edit ? <TextField/> : <h1 style={{margin: '0'}}>{milestone ? milestone.Name : ''}</h1>}
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
            <Typography style={{display: 'flex', flexDirection: `${edit ? 'column' : 'row'}`, justifyContent: 'left'}}> <b style={{marginRight: '0.25rem'}}>Ideal Completion:</b> {edit ? <DatePicker/> : 'mm/dd/yyyy'}</Typography>
            <Typography style={{display: 'flex', flexDirection: `${edit ? 'column' : 'row'}`, justifyContent: 'center'}}> <b style={{marginRight: '0.25rem'}}>Deadline:</b> {edit ? <DatePicker/> : 'mm/dd/yyyy'}</Typography>
            <Typography style={{display: 'flex', flexDirection: `${edit ? 'column' : 'row'}`, justifyContent: 'right'}}> <b style={{marginRight: '0.25rem'}}>Completed on:</b> {edit ? <DatePicker/> : 'mm/dd/yyyy'}</Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
              <Switch disabled={!edit}/>
              <Typography> Approved </Typography>
            </div>
            <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
              <Switch disabled={!edit}/>
              <Typography> Exempt </Typography>
            </div>
            <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
              <Switch disabled={!edit}/>
              <Typography> Completed </Typography>
            </div>
          </div>
          <div style={{ width: '100%' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tab} onChange={handleTabChange} aria-label="basic tabs example">
                <Tab label="Description"/>
                <Tab label="Notes"/>
              </Tabs>
            </Box>
            { tab === 0 &&
              <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '10rem'}}>
                <Typography>Placeholder text</Typography>
              </div>
            }
            { tab === 1 &&
              (edit ? 
                <textarea style={{resize: 'none', height: '10rem', width: 'calc(100% - 0.5rem)'}}/>
                :
                <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '10rem'}}>
                  <Typography>Placeholder text</Typography>
                </div>
              )
            }
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
          {edit ? <Button style={{position: 'absolute', right: '1rem', bottom: '1rem'}} variant='outlined' onClick={_ => (isNew ? checkNewFields(true) : setEdit(false))} disabled={checkChanged()}>Save</Button> : <></>}
          <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)}>
            <Box style={{width: '13.5%', backgroundColor: 'white', margin: '12.5% auto', padding: '1rem', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between'}}>
              <h2 style={{marginTop: '0'}}>Are you sure you want to delete this event?</h2>
              <Button variant='outlined' style={{marginRight: '1rem'}} onClick={_ => {if(!isNew){methods.removeMilestone(milestone.id)} setConfirmDelete(false); closeModal(null); setEdit(false)}}>Confrim</Button>
              <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>Keep Event</Button>
            </Box>
          </Modal>
        </Box>
      </Modal>
    )
  }

export default function  StudentMilestoneCard() {

    const [milestones, setMilestones] = useState([{Name: "First", id: 1}]);
    const [makeNew, setMakeNew] = useState(false);
    const [modal, setModal] = useState(null);

    var closeModal = _ => {
      setModal(null)
      setMakeNew(false)
    }
  
    var addMilestone = newMile => {
      setMilestones(milestones.concat(newMile))
      setMakeNew(false)
    }

    var removeMilestone = id => {
        setMilestones(milestones.filter( milestone => milestone.id != id))
    }

    var makeMilestoneCards = _ => {
        return milestones.map( (milestone, idx) => { return(
            <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid lightgray'}} onClick={_ => {setModal(milestone); setMakeNew(false)}} key={`milestone-${idx}`}>
                <h2 style={{margin: '0'}}>{milestone.Name}</h2>
                <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '0.25rem 0'}}>
                    <RadioButtonUncheckedIcon/>
                    <p style={{margin: '0', fontSize: '0.75rem'}}>Status</p>
                </div>
            </div>
        )
        })
    }

    return (
        <>
        <Card className="student-milestones-container">
            <CardContent>
                <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <strong>Milestones</strong>
                    <IconButton onClick={ _ => setMakeNew(true)}>
                        <AddCircleOutlineIcon sx={{color: '#630031'}}/>
                    </IconButton>
                </Typography>
                <div style={{overflowY: 'scroll', overflowX: 'hidden'}}>
                    <div className="student-milestones-placeholder">
                        {makeMilestoneCards()}
                    </div>
                </div>
            </CardContent>
        </Card>
        {MilestoneModal(modal, modal !== null, closeModal, {removeMilestone, addMilestone}, makeNew)}
        </>
    );
}
