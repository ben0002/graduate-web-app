import React, { useState, useEffect } from 'react';
import { TabPanel, MenuItem, Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, Tab, Tabs, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import { DatePicker } from '@mui/x-date-pickers';
import { useDispatch, useSelector } from 'react-redux';
import { apiRequest, isNumeric } from '../../assets/_commons';
import '../../assets/styling/student/studentRequirementCard';


function RequirementModal(requirement, openModal, closeModal, methods, newRequirement) {
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const [tab, setTab] = useState(0);
  const [localValues, setLocalValues] = useState({ name: '', description: '', ideal_completion_date: '', deadline: '', completion_date: '', approved: false, exempt: false, completed: false, note: '' });
  const dispatch = useDispatch();
  const student_id = useSelector(state => state.student.info.id)
  const [selectedMajorId, setSelectedMajorId] = useState('');
  const [selectedDegreeId, setSelectedDegreeId] = useState('');

  // Options for major and degree dropdowns
  const majorOptions = [
    { id: 1, name: 'ISE', description: 'Industrial & Systems Engineering' },
    { id: 2, name: 'SYSE', description: 'Systems Engineering' }
  ];

  const degreeOptions = [
    { id: 1, name: 'PHD', description: 'Doctor of Philosophy' },
    { id: 2, name: 'MS', description: 'Master of Science' },
    { id: 3, name: 'MENG', description: 'Master of Engineering' },
    { id: 4, name: 'MEA', description: 'Master of Engineering Administration' }
  ];

  useEffect(_ => {
    setIsNew(newRequirement);
    setEdit(newRequirement);
  }, [newRequirement])

  useEffect(() => {
    if (requirement) {
      setLocalValues({
        name: requirement.requirement.name,
        description: requirement.requirement.description,
        ideal_completion_date: requirement.ideal_completion_date,
        deadline: requirement.deadline,
        completion_date: requirement.completion_date,
        approved: requirement.approved,
        exempt: requirement.exempt,
        completed: requirement.completed,
        note: requirement.note
      });
      setSelectedMajorId(requirement.requirement.major_id ? requirement.requirement.major_id.toString() : '');
      setSelectedDegreeId(requirement.requirement.degree_id ? requirement.requirement.degree_id.toString() : '');
    } else {
      setLocalValues({
        name: '',
        description: '',
        ideal_completion_date: '',
        deadline: '',
        completion_date: '',
        approved: false,
        exempt: false,
        completed: false,
        note: ''
      });
      setSelectedMajorId('');
      setSelectedDegreeId('');
    }
  }, [requirement]);

  const handleDropdownChange = (event, type) => {
    const value = event.target.value;
    if (type === 'major') {
      setSelectedMajorId(value);
    } else if (type === 'degree') {
      setSelectedDegreeId(value);
    }
  };

  const checkChanged = _ => {
    if (isNew) {
      return true;
    } else {
      const requirementMajorId = requirement && requirement.requirement.major_id ? requirement.requirement.major_id.toString() : '';
      const requirementDegreeId = requirement && requirement.requirement.degree_id ? requirement.requirement.degree_id.toString() : '';

      return requirement && (
        localValues.name !== requirement.requirement.name ||
        localValues.description !== requirement.requirement.description ||
        localValues.ideal_completion_date !== requirement.ideal_completion_date ||
        localValues.deadline !== requirement.deadline ||
        localValues.completion_date !== requirement.completion_date ||
        localValues.approved !== requirement.approved ||
        localValues.exempt !== requirement.exempt ||
        localValues.completed !== requirement.completed ||
        localValues.note !== requirement.note ||
        selectedMajorId !== requirementMajorId ||
        selectedDegreeId !== requirementDegreeId
      )
    }
  }

  const checkValid = () => {
    return localValues.name.length > 0 &&
      selectedDegreeId.length > 0 &&
      selectedMajorId.length > 0 &&
      localValues.deadline;
  }

  const getDifferentValues = _ => {
    if (requirement == null || isNew) return {}
    let body = {}
    if (localValues.name !== requirement.name) body.name = localValues.name
    if (localValues.description !== requirement.description) body.description = localValues.description
    return body;
  }

  const handleInputChange = (name, value) => {
    setLocalValues(prevState => ({
      ...prevState,
      [name]: value
    }));
  }

  const handleTabChange = (_, newTab) => {
    setTab(newTab);
  };

  if (requirement == null && !isNew) { return (<></>) }

  return (
    <Modal open={openModal || isNew} onClose={_ => { closeModal(null); setEdit(false) }} className='flex flexCenter'>
      <div className='modalBox'>
        <div className='flex modalHeader'>
          {edit ? (
            <Box className='flex flexCenter modalHeaderForm'>
              <TextField
                label="Name"
                value={localValues.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                variant="outlined"
                style={{ width: '30rem' }}
              />
              <TextField
                select
                label="Major"
                value={selectedMajorId}
                onChange={(e) => handleDropdownChange(e, 'major')}
                variant="outlined"
                style={{ width: '8rem' }}
              >
                {majorOptions.map((option) => (
                  <MenuItem key={option.id} value={option.id}>{option.name}</MenuItem>
                ))}
              </TextField>
              <TextField
                select
                label="Degree"
                value={selectedDegreeId}
                onChange={(e) => handleDropdownChange(e, 'degree')}
                variant="outlined"
                style={{ width: '8rem' }}
              >
                {degreeOptions.map((option) => (
                  <MenuItem key={option.id} value={option.id}>{option.name}</MenuItem>
                ))}
              </TextField>
            </Box>
          ) : (
            <>
              <h1 style={{margin: '0'}}>{localValues.name}</h1>
              <Typography variant="body1">
                Major: {majorOptions.find(o => o.id === selectedMajorId)?.name || 'None'}
              </Typography>
              <Typography variant="body1">
                Degree: {degreeOptions.find(o => o.id === selectedDegreeId)?.name || 'None'}
              </Typography>
            </>
          )}
          {/*<div style={{ display: 'flex' }}>
            <IconButton onClick={_ => setEdit(!edit)}>
              <EditIcon sx={{ color: '#630031' }} />
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <HighlightOffIcon sx={{ color: '#630031' }} />
            </IconButton>
          </div>*/}
        </div>
        <div className='flex flexCenter modalBody'>
          <Typography style={{ display: 'flex', flexDirection: `${edit ? 'column' : 'row'}`, justifyContent: 'left' }}> <b style={{ marginRight: '0.25rem' }}>Ideal Completion:</b> {edit ? <DatePicker /> : localValues.ideal_completion_date || 'N/A'}</Typography>
          <Typography style={{ display: 'flex', flexDirection: `${edit ? 'column' : 'row'}`, justifyContent: 'center' }}> <b style={{ marginRight: '0.25rem' }}>Deadline:</b> {edit ? <DatePicker /> : localValues.deadline || 'N/A'}</Typography>
          <Typography style={{ display: 'flex', flexDirection: `${edit ? 'column' : 'row'}`, justifyContent: 'right' }}> <b style={{ marginRight: '0.25rem' }}>Completed on:</b> {edit ? <DatePicker /> : localValues.completion_date  || 'N/A'}</Typography>
        </div>
        <div className='flex flexCenter modalBody'>
          <div className='flex flexCenter'>
            <Switch disabled={!edit} checked={localValues.approved}/>
            <Typography> Approved </Typography>
          </div>
          <div className='flex flexCenter'>
            <Switch disabled={!edit} checked={localValues.exempt}/>
            <Typography> Exempt </Typography>
          </div>
          <div className='flex flexCenter'>
            <Switch disabled={!edit} checked={localValues.completed}/>
            <Typography> Completed </Typography>
          </div>
        </div>
        <div className='fullWidth'>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tab} onChange={handleTabChange} aria-label="basic tabs example">
              <Tab label="Description" />
              <Tab label="Notes" />
            </Tabs>
          </Box>
          { tab === 0 &&
            (edit ? 
              <textarea name="description" value={localValues.description} className='modalTextArea'/>
              :
              <div className='modalDescription'>
                <Typography>{localValues.description}</Typography>
              </div>
            )
          }
          { tab === 1 &&
            (edit ? 
              <textarea name="notes" value={localValues.notes} className='modalTextArea'/>
              :
              <div className='modalDescription'>
                <Typography>{localValues.notes}</Typography>
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
        {edit ? (
          <Button
            className='saveButton actionButton'
            variant='outlined'
            onClick={() => {
              let body, apiEndpoint, apiMethod;

              if (isNew) {
                body = {
                  ...localValues,
                  student_id: student_id,
                  degree_id: parseInt(selectedDegreeId),
                  major_id: parseInt(selectedMajorId)
                };
                apiEndpoint = 'requirement';
                apiMethod = 'POST';
              } else {
                body = {};
                if (localValues.name !== requirement.name) body.name = localValues.name;
                if (localValues.description !== requirement.description) body.description = localValues.description;  

                apiEndpoint = 'requirement/${requirement.id}';
                apiMethod = 'PATCH'
              }

              apiRequest(apiEndpoint, apiMethod, body)
                .then(res => {
                  if (res.ok) return res.json();
                  else throw new Error(`HTTP error! status: ${res.status}`);
                })
                .then(data => {
                  if (!data) throw new Error('Error: Non-ok HTTP response');
                  if (isNew) {
                    dispatch({ type: 'add_requirement', payload: data });
                  } else {
                    dispatch({ type: 'update_requirement', payload: data });
                  }
                  setIsNew(false);
                  setEdit(false);
                  closeModal();
                })
                .catch(err => {
                  console.error('Error:', err.message);
                });
            }}
            enabled={!checkChanged() || !checkValid()}
          >
            Save
          </Button>

        ) : (
          <></>
        )}
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)} className='flex flexCenter'>
          <div className="flex flexColumn flexWrap flexCenter modalBox">
            <h2>Are you sure you want to delete this event?</h2>
            <Button variant='outlined' style={{ marginRight: '1rem' }} onClick={_ => { if (!isNew) { methods.removeRequirement(milestone.id) } setConfirmDelete(false); closeModal(null); setEdit(false) }}>Confrim</Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>Keep Event</Button>
          </div>
        </Modal>
      </div>
    </Modal >
  )
}

export default function StudentrequirementCard() {

  const [makeNew, setMakeNew] = useState(false);
  const [modal, setModal] = useState(null);
  const requirements = useSelector(state => state.student.requirements);
  const dispatch = useDispatch();

  var closeModal = _ => {
    setModal(null)
    setMakeNew(false)
  }

  var addRequirement = newMile => {
    setrequirement(requirement.concat(newMile))
    setMakeNew(false)
  }

  var removeRequirement = id => {
    setrequirement(requirement.filter(requirement => requirement.id != id))
  }

  const deleteRequirement = (requirementId) => {
    apiRequest(`requirement/${requirementId}`, 'DELETE', {})
      .then(res => {
        if (res.ok) {
    
          dispatch({ type: 'remove_requirement', payload: requirementId });
        } else {
          console.error(`Failed to delete requirement with ID: ${requirementId}`);
        }
      })
      .catch(err => console.error('Error:', err));
  }

  var makeRequirementCards = _ => {
    return requirements.map((requirement) => {
      return (
        <div className='flex flexCenter requirementCardItem'>
          <h2>{requirement.requirement.name}</h2>
          <div className='flex flexColumn flexCenter statusContainer'>
            <RadioButtonUncheckedIcon />
            <p>Status</p>
          </div>
        </div>
      )
    })
  }

    return (
        <>
        <Card className="studentRequirementsContainer">
            <CardContent>
                <Typography variant="h6" component="div" className='flex'>
                    <strong>Requirements</strong>
                    {/*<IconButton onClick={ _ => setMakeNew(true)}>
                        <AddCircleOutlineIcon sx={{color: '#630031'}}/>
                    </IconButton>*/}
                </Typography>
                <div className='overflowY'>
                    <div className="studentRequirementList">
                        {makeRequirementCards()}
                    </div>
                </div>
            </CardContent>
        </Card>
        {RequirementModal(modal, modal !== null, closeModal, {removeRequirement, addRequirement}, makeNew)}
        </>
    );
}
