import React, { useState, useEffect } from 'react';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, Tab, Tabs, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { DatePicker } from '@mui/x-date-pickers';
import { useDispatch, useSelector } from 'react-redux';
import dayjs from 'dayjs';
import { apiRequest, isNumeric } from '../../assets/_commons';
import '../../assets/styling/student/studentFundingCard';

function FundingModal(funding, openModal, closeModal, newFunding){
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [localValues, setLocalValues] = useState({name: '', award_amount: 0, start_date: '', end_date: '', guaranteed: false, recurring: false, description: '', notes: ''});
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [tab, setTab] = useState(0);
  const dispatch = useDispatch();
  const student_id = useSelector(state => state.student.info.id)

  useEffect(_ => {
    setIsNew(newFunding);
    setEdit(newFunding);
  }, [newFunding])

  useEffect(_=>{
    if(funding) setLocalValues({name: funding.name, award_amount: funding.award_amount, start_date: funding.start_date, end_date: funding.end_date, guaranteed: funding.guaranteed, recurring: funding.recurring, description: funding.description, notes: funding.notes})
    else setLocalValues({name: '', award_amount: 0, start_date: '', end_date: '', guaranteed: false, recurring: false, description: '', notes: ''})
  }, [funding])

  const checkChanged = _ => {
    return funding && (
      localValues.name !== funding.name || 
      localValues.award_amount !== funding.award_amount || 
      localValues.start_date !== funding.start_date || 
      localValues.end_date !== funding.end_date || 
      localValues.guaranteed !== funding.guaranteed ||
      localValues.recurring !== funding.recurring ||
      localValues.description !== funding.description ||
      localValues.notes !== funding.notes
      )
  }

  const checkValid = _ => {
    return (
      localValues.name.length > 0 &&
      localValues.award_amount >= 0 &&
      localValues.start_date.length > 0 &&
      localValues.end_date.length > 0 &&
      localValues.guaranteed != null  &&
      localValues.recurring != null
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
    if(localValues.recurring !== funding.recurring) body.recurring = localValues.recurring
    if(localValues.description !== funding.description) body.description = localValues.description
    if(localValues.notes !== funding.notes) body.notes = localValues.notes
    return body
  }

  const handleTabChange = (_, newTab) => {
    setTab(newTab);
  };

  const handleInputChange = target => {
    switch(target.name){
      case 'recurring':
      case 'guaranteed':
        setLocalValues({...localValues, [target.name]: target.checked})
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
      <Modal open={openModal || isNew} onClose={_ => {closeModal(); setEdit(false); setIsNew(false); setLocalValues({name: '', award_amount: 0, start_date: '', end_date: '', guaranteed: false, recurring: false, description: '', notes: ''})}} className='flex flexCenter'>
      <div className='modalBox'>
        <div className='flex modalHeader'>
          {edit ? <TextField label="Name" name="name" value={localValues.name} onChange={e => handleInputChange(e.target)}/> : <h1>{funding.name || ''}</h1>}
          <div className='flex'>
            <IconButton onClick={_ => (isNew ? checkValid() ? setConfirmDelete(true) : closeModal() : setEdit(!edit))}>
              <EditIcon sx={{color: '#630031'}}/>
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <DeleteIcon sx={{color: '#630031'}}/>
            </IconButton>
          </div>
        </div>
        <div className='flex flexCenter modalBody'>
          <div className='flex flexColumn flexCenter modalBody'>
            <Typography className='flex flexCenter modalBodyText'><b>Total:</b> {edit ? <TextField label="Award Amount" name="award_amount" value={localValues.award_amount} onChange={e => handleInputChange(e.target)}/> : `$${funding.award_amount}`}</Typography>
            <Typography className='flex flexCenter modalBodyText'><b>Recurring:</b> <Switch disabled={!edit} checked={localValues.recurring} name="recurring" onChange={e => handleInputChange(e.target)}/></Typography>
          </div>
          <div className='flex flexColumn modalBody modalBodyDates'>
            <Typography className='flex flexCenter modalBodyText'><b>Start Date:</b> {edit ? <DatePicker name="start_date" value={localValues.start_date.length == 0 ? null : dayjs(localValues.start_date)} onChange={e => setLocalValues({...localValues, start_date: dayjs(e).format('YYYY-MM-DD')})}/> : funding.start_date}</Typography>
            <Typography className='flex flexCenter modalBodyText'><b>End Date:</b> {edit ? <DatePicker name="end_date" value={localValues.end_date.length == 0 ? null : dayjs(localValues.end_date)} onChange={e => setLocalValues({...localValues, end_date: dayjs(e).format('YYYY-MM-DD')})}/> : funding.end_date}</Typography>
          </div>
          <div className='flex flexCenter'>
            <Switch disabled={!edit} checked={localValues.guaranteed} name="guaranteed" onChange={e => handleInputChange(e.target)}/>
            <Typography> Gauranteed </Typography>
          </div>
        </div>
        <div className='fullWidth'>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tab} onChange={handleTabChange} aria-label="basic tabs example">
              <Tab label="Description"/>
              <Tab label="Notes"/>
            </Tabs>
          </Box>
          { tab === 0 &&
            (edit ? 
              <textarea name="description" value={localValues.description} onChange={e => handleInputChange(e.target)} className='modalTextArea'/>
              :
              <div className='modalDescription'>
                <Typography>{funding.description}</Typography>
              </div>
            )
          }
          { tab === 1 &&
            (edit ? 
              <textarea name="notes" value={localValues.notes} onChange={e => handleInputChange(e.target)} className='modalTextArea'/>
              :
              <div className='modalDescription'>
                <Typography>{funding.notes}</Typography>
              </div>
            )
          }
        </div>
        <div className='fileSection'>
          <div className='flex flexCenter'>
            <h3 className='fileSectionHeader'> Files: </h3>
            <Button component='label' startIcon={<FileUploadIcon sx={{ color: '#630031' }} />}>
              <Input type='file' className='hiddenInput' onChange={e => console.log(e.target.files)} />
            </Button>
          </div>
          <div className='fileDisplay'>
            <h3>File1.pdf</h3>
          </div>
        </div>
        {edit ?
          <Button
            className='saveButton actionButton' 
            onClick={_ => {
              if(isNew){
                var body = {...localValues};
                apiRequest(`students/${student_id}/funding`, 'POST', body)
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
                apiRequest(`student/${student_id}/funding/${funding.id}`, 'PATCH', getDifferentValues())
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
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)} className='flex flexCenter'>
        <div className="flex flexColumn flexWrap flexCenter modalBox">
            <h2>Are you sure you want to delete this event?</h2>
            <Button variant='outlined' style={{marginRight: '1rem'}} 
              onClick={_ => {
                if(!isNew){
                  apiRequest(`students/${student_id}/funding/${funding.id}`, 'DELETE', null)
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
          </div>
        </Modal>
      </div>
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
      <div className='flex flexColumn fundingItem' onClick={_ => {setModal(funding); setMakeNew(false)}} key={`funding-${funding.id}`}>
        <div className='flex flexCenter flexWrap'>
          <h2>{funding.name}</h2>
          <p>${funding.award_amount}</p>
        </div>
        <div>
          <p className='fundingItemDate'>{funding.start_date} -</p>
          <p className='fundingItemDate'>{funding.end_date}</p>
        </div>
      </div>
    )})
  }

  return (
    <>
    <Card className="studentFundingContainer">
      <CardContent>
        <Typography variant="h6" component="div" className='flex'>
          <strong>Student Funding</strong>
          <IconButton onClick={ _ => setMakeNew(true)}>
            <AddCircleOutlineIcon sx={{color: '#630031'}}/>
          </IconButton>
        </Typography>
        <div className='overflowY studentFundingListContainer'>
          <div className="flex flexColumn flexCenter studentFundingList">
            {makeFundingCards()}
          </div>
        </div>
      </CardContent>
    </Card>
    {FundingModal(modal, modal !== null, closeModal, makeNew)}
    </>
  );
};