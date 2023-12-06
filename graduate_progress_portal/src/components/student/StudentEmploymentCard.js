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
import '../../assets/styling/student/studentEmploymentCard';

function EmploymentModal(employment, openModal, closeModal, newEmployment){
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [localValues, setLocalValues] = useState({employer: '', job_title: '', pay: '', start_date: '', end_date: '', type: '', description: '', notes: ''});
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [tab, setTab] = useState(0);
  const student_id = useSelector(state => state.student.info.id)
  const dispatch = useDispatch();

  useEffect(_ => {
    setIsNew(newEmployment);
    setEdit(newEmployment);
  }, [newEmployment])

  useEffect(_=>{
    if(employment) setLocalValues({employer: employment.employer, job_title: employment.job_title, pay: employment.pay, start_date: employment.start_date, end_date: employment.end_date, type: employment.type, description: employment.description, notes: employment.notes})
    else setLocalValues({employer: '', job_title: '', pay: 0, start_date: '', end_date: '', type: '', description: '', notes: ''})
  }, [employment])

  const checkChanged = _ => {
    return employment && (
      localValues.employer !== employment.employer ||
      localValues.job_title !== employment.job_title || 
      localValues.pay !== employment.pay || 
      localValues.start_date !== employment.start_date || 
      localValues.end_date !== employment.end_date || 
      localValues.type !== employment.type ||
      localValues.description !== employment.description ||
      localValues.notes !== employment.notes 
      )
  }

  const checkValid = _ => {
    return (
      localValues.employer.length > 0 &&
      localValues.job_title.length > 0 &&
      localValues.pay >= 0 &&
      localValues.start_date.length > 0 &&
      localValues.end_date.length > 0 &&
      localValues.type.length > 0
    )
  }

  const getDifferentValues = _ => {
    if(employment == null) return {}
    var body = {}
    if(localValues.employer !== employment.employer) body.employer = localValues.employer
    if(localValues.job_title !== employment.job_title) body.job_title = localValues.job_title
    if(localValues.pay !== employment.pay) body.pay = localValues.pay
    if(localValues.start_date !== employment.start_date) body.start_date = localValues.start_date
    if(localValues.end_date !== employment.end_date) body.end_date = localValues.end_date
    if(localValues.type !== employment.type) body.type = localValues.type
    if(localValues.description !== employment.description) body.description = localValues.description
    if(localValues.notes !== employment.notes) body.notes = localValues.notes
    return body
  }

  const handleTabChange = (_, newTab) => {
    setTab(newTab);
  };

  const handleInputChange = target => {
    switch(target.name){
      case 'pay':
        if(isNumeric(target.value)) setLocalValues({...localValues, pay: +target.value})
        break
      default:
        setLocalValues({...localValues, [target.name]: target.value})
    }
  }

  if(employment == null && !isNew) {return(<></>)}

    return(
      <Modal open={openModal || isNew} onClose={_ => {closeModal(); setEdit(false); setIsNew(false)}} className='flex flexCenter'>
      <div className='modalBox'>
        <div className='flex flexCenter modalHeader'>
         {edit ? <div> <b><TextField label="Employer" name="employer" value={localValues.employer} onChange={e => handleInputChange(e.target)}/> -</b> <TextField label="Job Title" name="job_title" value={localValues.job_title} onChange={e => handleInputChange(e.target)}/></div>: <h1>{employment.employer || 'Company'} - {employment.job_title}</h1>}
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
          <div className='flex flexColumn modalBody' style={{alignItems: `${edit ? 'end' : 'start'}`}}>
            <Typography className='flex flexCenter modalBodyText'><b>Salary:</b> {edit ? <TextField label="Pay" name="pay" value={localValues.pay} onChange={e => handleInputChange(e.target)}/> : `$${employment.pay}`}</Typography>
            <Typography className='flex flexCenter modalBodyText'><b>Empl. Type:</b> {edit ? <TextField label="Employment Type" name="type" value={localValues.type} onChange={e => handleInputChange(e.target)}/> : employment.type}</Typography>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'end', justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b>Start Date:</b> {edit ? <DatePicker value={localValues.start_date.length == 0 ? null : dayjs(localValues.start_date)} onChange={e => setLocalValues({...localValues, start_date: dayjs(e).format('YYYY-MM-DD')})}/> : employment.start_date}</Typography>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b>End Date:</b> {edit ? <DatePicker value={localValues.end_date.length == 0 ? null : dayjs(localValues.end_date)} onChange={e => setLocalValues({...localValues, end_date: dayjs(e).format('YYYY-MM-DD')})}/> : employment.end_date}</Typography>
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
                <Typography>{employment.description}</Typography>
              </div>
            )
          }
          { tab === 1 &&
            (edit ? 
              <textarea name="notes" value={localValues.notes} onChange={e => handleInputChange(e.target)} className='modalTextArea'/>
              :
              <div className='modalDescription'>
                <Typography>{employment.notes}</Typography>
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
          <Button className='saveButton actionButton' variant='outlined' onClick={_ => {
            if(isNew){
              var body = {...localValues};
              apiRequest(`students/${student_id}/employments`, 'POST', body)
              .then(res => {
                if(res.ok) return res.json();
                else console.log(res.status);
              })
              .then(data => {
                if (data == undefined) console.error('Error: Non ok http response');
                else{
                    dispatch({type: 'add_employment', payload: data})
                }
              })
              .catch((err) => console.error('Error:', err.message))
            }
            else{ 
              apiRequest(`student/${student_id}/employments/${employment.id}`, 'PATCH', getDifferentValues())
              .then(res => {
                if(res.ok) return res.json();
                else console.log(res.status);
              })
              .then(data => {
                if (data == undefined) console.error('Error: Non ok http response');
                else{
                    dispatch({type: 'update_employment', payload: {id: employment.id, data}})
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
                  apiRequest(`students/${student_id}/employments/${employment.id}`, 'DELETE', null)
                  .then(res => {
                    if(res.ok) return res.json();
                    else console.log(res.status);
                  })
                  .then(data => {
                    if (data == undefined) console.error('Error: Non ok http response');
                    else{
                        dispatch({type: 'delete_employment', payload: {id: employment.id}})
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

export default function StudentEmploymentCard() {

  const [makeNew, setMakeNew] = useState(false);
  const [modal, setModal] = useState(null);

  const employments = useSelector( state => state.student.employment)

  var closeModal = _ => {
    setModal(null)
    setMakeNew(false)
  }

  var makeEmploymentCards = _ => {
    return employments.map( employment => { return(
      <div className='flex flexColumn employmentItem' onClick={_ => {setModal(employment); setMakeNew(false)}} key={`employment-${employment.id}`}>
        <div className='flex flexCenter flexWrap'>
          <h2>{employment.job_title}</h2>
          <p>${employment.pay}</p>
        </div>
        <div>
          <p className='employmentItemDate'>{employment.start_date} -</p>
          <p className='employmentItemDate'>{employment.end_date}</p>
        </div>
      </div>
    )})
  }

  return (
    <>
    <Card className="studentEmploymentContainer">
      <CardContent>
        <Typography variant="h6" component="div" className='flex'>
          <strong>Student Employment</strong>
          <IconButton onClick={ _ => setMakeNew(true)}>
            <AddCircleOutlineIcon sx={{color: '#630031'}}/>
          </IconButton>
        </Typography>
        <div className='overflowY studentEmploymentListContainer'>
          <div className="flex flexColumn flexCenter studentEmploymentList">
            {makeEmploymentCards()}
          </div>
        </div>
      </CardContent>
    </Card>
    {EmploymentModal(modal, modal !== null, closeModal, makeNew)}
    </>
  );
};
