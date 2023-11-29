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

function EmploymentModal(employment, openModal, closeModal, newEmployment){
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [localValues, setLocalValues] = useState({job_title: '', pay: '', start_date: '', end_date: '', type: ''});
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [tab, setTab] = useState(0);
  const student_id = useSelector(state => state.student.info.id)
  const dispatch = useDispatch();

  useEffect(_ => {
    setIsNew(newEmployment);
    setEdit(newEmployment);
  }, [newEmployment])

  useEffect(_=>{
    if(employment) setLocalValues({job_title: employment.job_title, pay: employment.pay, start_date: employment.start_date, end_date: employment.end_date, type: employment.type})
    else setLocalValues({job_title: '', pay: 0, start_date: '', end_date: '', type: ''})
  }, [employment])

  const checkChanged = _ => {
    return employment && (
      localValues.job_title !== employment.job_title || 
      localValues.pay !== employment.pay || 
      localValues.start_date !== employment.start_date || 
      localValues.end_date !== employment.end_date || 
      localValues.type !== employment.type
      )
  }

  const checkValid = _ => {
    return (
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
    if(localValues.job_title !== employment.job_title) body.job_title = localValues.job_title
    if(localValues.pay !== employment.pay) body.pay = localValues.pay
    if(localValues.start_date !== employment.start_date) body.start_date = localValues.start_date
    if(localValues.end_date !== employment.end_date) body.end_date = localValues.end_date
    if(localValues.type !== employment.type) body.type = localValues.type
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
  
  //console.log((!checkChanged() || isNew) && !checkValid())
  //console.log(!checkChanged())
  //console.log(isNew)
  //console.log(!checkValid())
  console.log("skip")

    return(
      <Modal open={openModal || isNew} onClose={_ => {closeModal(); setEdit(false); setIsNew(false)}}>
      <Box style={{width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
         {edit ? <div> <b style={{fontSize: '2rem'}}>Company -</b> <TextField name="job_title" value={localValues.job_title} onChange={e => handleInputChange(e.target)}/></div>: <h1 style={{margin: '0'}}>Company - {employment.job_title}</h1>}
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
            <p style={{margin: '0', display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Salary:</b> {edit ? <TextField name="pay" value={localValues.pay} onChange={e => handleInputChange(e.target)}/> : `$${employment.pay}`}</p>
            <p style={{margin: '0', display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Empl. Type:</b> {edit ? <TextField name="type" value={localValues.type} onChange={e => handleInputChange(e.target)}/> : employment.type}</p>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'end', justifyContent: 'space-between', paddingRight: '.75rem'}}>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>Start Date:</b> {edit ? <DatePicker value={localValues.start_date.length == 0 ? null : dayjs(localValues.start_date)} onChange={e => setLocalValues({...localValues, start_date: dayjs(e).format('YYYY-MM-DD')})}/> : employment.start_date}</Typography>
            <Typography style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}><b style={{marginRight: '0.25rem'}}>End Date:</b> {edit ? <DatePicker value={localValues.end_date.length == 0 ? null : dayjs(localValues.end_date)} onChange={e => setLocalValues({...localValues, end_date: dayjs(e).format('YYYY-MM-DD')})}/> : employment.end_date}</Typography>
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
        {edit ? <Button style={{position: 'absolute', right: '1rem', bottom: '1rem'}} variant='outlined' 
          onClick={_ => {
            if(isNew){
              var body = {...localValues};
              body.student_id = student_id
              apiRequest(`student/employment`, 'POST', body)
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
              apiRequest(`student/employment/${employment.id}`, 'PUT', getDifferentValues())
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
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)}>
          <Box style={{width: '13.5%', backgroundColor: 'white', margin: '12.5% auto', padding: '1rem', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between'}}>
            <h2 style={{marginTop: '0'}}>Are you sure you want to delete this event?</h2>
            <Button variant='outlined' style={{marginRight: '1rem'}}
              onClick={_ => {
                if(!isNew){
                  apiRequest(`student/employment/${employment.id}`, 'DELETE', null)
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
          </Box>
        </Modal>
      </Box>
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
      <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', borderBottom: '1px solid lightgray'}} onClick={_ => {setModal(employment); setMakeNew(false)}} key={`employment-${employment.id}`}>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap'}}>
          <h2 style={{margin: '0'}}>{employment.job_title}</h2>
          <p style={{margin: '0'}}>${employment.pay}</p>
        </div>
        <div>
          <p style={{margin: '0', fontSize: '0.75rem', display: 'inline-block'}}>{employment.start_date} -</p>
          <p style={{margin: '0', fontSize: '0.75rem', display: 'inline-block'}}>{employment.end_date}</p>
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
          <IconButton onClick={ _ => setMakeNew(true)}>
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
    {EmploymentModal(modal, modal !== null, closeModal, makeNew)}
    </>
  );
};
