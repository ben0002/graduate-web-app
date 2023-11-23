import React, { useState } from 'react';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';

var count = 2;

function FundingModal(funding, openModal, closeModal, removeFunding){
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  if(funding == null) return(<></>)

  return(
    <Modal open={openModal} onClose={_ => closeModal(null)}>
      <Box style={{width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
        <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
          <h1 style={{margin: '0'}}>{funding.Name}</h1>
          <div style={{display: 'flex'}}>
            <IconButton onClick={_ => removeFunding(funding.id)}>
              <EditIcon sx={{color: '#630031'}}/>
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <HighlightOffIcon sx={{color: '#630031'}}/>
            </IconButton>
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingRight: '.75rem'}}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'start', justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <p style={{margin: '0'}}><b>Total:</b>  $$$$$</p>
            <p style={{margin: '0'}}><b>Recurring:</b> No/Period</p>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'start', justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <Typography> <b>Start Date:</b> mm/dd/yyyy</Typography>
            <Typography> <b>End Date:</b> mm/dd/yyyy</Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch/>
            <Typography> Approved </Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch/>
            <Typography> Gauranteed </Typography>
          </div>
        </div>
        {/* POSSIBLY CONVERT TO TABS */}
        <h3 style={{margin: '0.25rem 0'}}>Description:</h3>
        <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '7rem'}}>
          <Typography>Placeholder text</Typography>
        </div>
        <h3 style={{margin: '0.25rem 0'}}>Notes:</h3>
        <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '7rem'}}>
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
            <Button variant='outlined' style={{marginRight: '1rem'}} onClick={_ => {removeFunding(funding.id); setConfirmDelete(false); closeModal(null)}}>Confrim</Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>Keep Event</Button>
          </Box>
        </Modal>
      </Box>
    </Modal>
  )
}

export default function StudentFundingCard() {

  const [fundings, setFundings] = useState([{Name: "First", id: 1}]);
  const [modal, setModal] = useState(null);

  var addFunding = _ => {
    setFundings(fundings.concat({Name: `${count}`, id: count}))
    count += 1;
  }

  var removeFunding = id => {
    setFundings(fundings.filter( funding => funding.id != id))
  }

  var makeFundingCards = _ => {
    return fundings.map( funding => { return(
      <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', borderBottom: '1px solid lightgray'}} onClick={_ => setModal(funding)}>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between'}}>
          <h2 style={{margin: '0'}}>{funding.Name}</h2>
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
    <Card className="student-funding-card-container">
      <CardContent>
        <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
          <strong>Student Funding</strong>
          <IconButton onClick={ _ => addFunding()}>
            <AddCircleOutlineIcon sx={{color: '#630031'}}/>
          </IconButton>
        </Typography>
        <div style={{overflowY: 'scroll', overflowX: 'hidden', minHeight: '17.5rem', maxHeight: '17.5rem'}}>
          <div className="student-funding-card-placeholder">
            {makeFundingCards()}
          </div>
        </div>
      </CardContent>
    </Card>
    {FundingModal(modal, modal !== null, setModal, removeFunding)}
    </>
  );
};