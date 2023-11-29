import React, { useState, useEffect } from 'react';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, Tab, Tabs, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { DatePicker } from '@mui/x-date-pickers';
import { useDispatch, useSelector } from 'react-redux';
import dayjs from 'dayjs';
import { apiRequest, isNumeric } from '../../assets/_commons';

function FundingModal(funding, openModal, closeModal, newFunding){
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [localValues, setLocalValues] = useState({name: '', award_amount: '', start_date: '', end_date: '', guaranteed: false});
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [tab, setTab] = useState(0);
  const dispatch = useDispatch();
  const student_id = useSelector(state => state.student.info.id)

  useEffect(_ => {
    setIsNew(newFunding);
    setEdit(newFunding);
  }, [newFunding])

  useEffect(_=>{
    if(funding) setLocalValues({name: funding.name, award_amount: funding.award_amount, start_date: funding.start_date, end_date: funding.end_date, guaranteed: funding.guaranteed})
    else setLocalValues({name: '', award_amount: '', start_date: null, end_date: null, guaranteed: false})
  }, [funding])

  const checkChanged = _ => {
    return funding && (
      localValues.name !== funding.name || 
      localValues.award_amount !== funding.award_amount || 
      localValues.start_date !== funding.start_date || 
      localValues.end_date !== funding.end_date || 
      localValues.guaranteed !== funding.guaranteed
      )
  }

  const checkValid = _ => {
    return (
      localValues.name.length > 0 &&
      localValues.award_amount >= 0 &&
      localValues.start_date.length > 0 &&
      localValues.end_date.length > 0 &&
      localValues.guaranteed != null
    )
  }

  const getDifferentValues = _ => {
    if(funding == null) return {}
    var body = {}
    if(localValues.name !== funding.name) body.name = localValues.name
    if(localValues.award_amount !== funding.award_amount) body.award_amount = localValues.award_amount
    if(localValues.start_date !== funding.start_date) body.start_date = localValues.start_date
    if(localValues.end_date !== funding.end_date) body.end_date = localValues.end_date
    if(localValues.guaranteed !== funding.guaranteed) body.guaranteed = localValues.guaranteed
    return body
  }

  const handleTabChange = (_, newTab) => {
    setTab(newTab);
  };

  const handleInputChange = target => {
    switch(target.name){
      case 'guaranteed':
        setLocalValues({...localValues, guaranteed: target.checked})
        break
      case 'award_amount':
        if(isNumeric(target.value)) setLocalValues({...localValues, award_amount: +target.value})
        break
      default:
        setLocalValues({...localValues, [target.name]: target.value})
    }
  }

  if(funding == null && !isNew) {return(<></>)}

    return(
      <Modal open={openModal || isNew} onClose={_ => {closeModal(); setEdit(false); setIsNew(false)}}>
      <Box style={{width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
        <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
          {edit ? <TextField name="name" value={localValues.name} onChange={e => handleInputChange(e.target)}/> : <h1 style={{margin: '0'}}>{funding.name || ''}</h1>}
          <div style={{display: 'flex'}}>
            <IconButton onClick={_ => (isNew ? checkValid() ? setConfirmDelete(true) : closeModal() : setEdit(!edit))}>
              <EditIcon sx={{color: '#630031'}}/>
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <HighlightOffIcon sx={{color: '#630031'}}/>
            </IconButton>
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingRight: '.75rem'}}>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: `${edit ? 'end' : 'start'}`, justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <p style={{margin: '0', display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Total:</b> {edit ? <TextField name="award_amount" value={localValues.award_amount} onChange={e => handleInputChange(e.target)}/> : `$${funding.award_amount}`}</p>
            <p style={{margin: '0', display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Recurring:</b> {edit ? <TextField/> : 'No/Period'}</p>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'end', justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Start Date:</b> {edit ? <DatePicker name="start_date" value={localValues.start_date} onChange={e => setLocalValues({...localValues, start_date: dayjs(e).format('YYYY-MM-DD')})}/> : funding.start_date}</Typography>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>End Date:</b> {edit ? <DatePicker name="end_date" value={localValues.end_date} onChange={e => setLocalValues({...localValues, end_date: dayjs(e).format('YYYY-MM-DD')})}/> : funding.end_date}</Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch disabled={!edit}/>
            <Typography> Approved </Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
            <Switch disabled={!edit} checked={localValues.guaranteed} name="guaranteed" onChange={e => handleInputChange(e.target)}/>
            <Typography> Gauranteed </Typography>
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
            (edit ? 
              <textarea style={{resize: 'none', height: '10rem', width: 'calc(100% - 0.5rem)'}}/>
              :
              <div style={{borderTop: '1px solid lightgray', borderBottom: '1px solid lightgray', borderRadius: '0.5rem', height: '10rem'}}>
                <Typography>Placeholder text</Typography>
              </div>
            )
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
        {edit ? 
          <Button style={{position: 'absolute', right: '1rem', bottom: '1rem'}} variant='outlined' 
          onClick={_ => {
            if(isNew){
              var body = {...localValues};
              body.student_id = student_id
              apiRequest(`student/funding`, 'POST', body)
              .then(res => {
                if(res.ok) return res.json();
                else console.log(res.status);
              })
              .then(data => {
                if (data == undefined) console.error('Error: Non ok http response');
                else{
                    dispatch({type: 'add_funding', payload: data})
                }
              })
              .catch((err) => console.error('Error:', err.message))
            }
            else{ 
              apiRequest(`student/funding/${funding.id}`, 'PUT', getDifferentValues())
              .then(res => {
                if(res.ok) return res.json();
                else console.log(res.status);
              })
              .then(data => {
                if (data == undefined) console.error('Error: Non ok http response');
                else{
                    dispatch({type: 'update_funding', payload: {id: funding.id, data}})
                }
              })
              .catch((err) => console.error('Error:', err.message))
            }
            setIsNew(false)
            setEdit(false)
            closeModal()
          }} 
          disabled={(!checkChanged() || isNew) && !checkValid()}>Save</Button> 
          : 
          <></>
        }
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)}>
          <Box style={{width: '13.5%', backgroundColor: 'white', margin: '12.5% auto', padding: '1rem', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <h2 style={{marginTop: '0'}}>Are you sure you want to delete this event?</h2>
            <Button variant='outlined' style={{marginRight: '1rem'}} 
              onClick={_ => {
                if(!isNew){
                  apiRequest(`student/funding/${funding.id}`, 'DELETE', null)
                  .then(res => {
                    if(res.ok) return res.json();
                    else console.log(res.status);
                  })
                  .then(data => {
                    if (data == undefined) console.error('Error: Non ok http response');
                    else{
                        dispatch({type: 'delete_funding', payload: {id: funding.id}})
                    }
                  })
                  .catch((err) => console.error('Error:', err.message))
                } setConfirmDelete(false); closeModal(); setEdit(false)}}>Confrim</Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>Keep Event</Button>
          </Box>
        </Modal>
      </Box>
    </Modal>
  )
}

export default function StudentFundingCard() {

  const [makeNew, setMakeNew] = useState(false);
  const [modal, setModal] = useState(null);

  const fundings = useSelector( state => state.student.funding)

  var closeModal = _ => {
    setModal(null)
    setMakeNew(false)
  }

  console.log(fundings)

  var makeFundingCards = _ => {
    return fundings.map( funding => { return(
      <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', borderBottom: '1px solid lightgray'}} onClick={_ => {setModal(funding); setMakeNew(false)}} key={`funding-${funding.id}`}>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap'}}>
          <h2 style={{margin: '0'}}>{funding.name}</h2>
          <p style={{margin: '0'}}>${funding.award_amount}</p>
        </div>
        <div>
          <p style={{margin: '0', fontSize: '0.75rem', display: 'inline-block'}}>{funding.start_date} -</p>
          <p style={{margin: '0', fontSize: '0.75rem', display: 'inline-block'}}>{funding.end_date}</p>
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
          <IconButton onClick={ _ => setMakeNew(true)}>
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
    {FundingModal(modal, modal !== null, closeModal, makeNew)}
    </>
  );
};