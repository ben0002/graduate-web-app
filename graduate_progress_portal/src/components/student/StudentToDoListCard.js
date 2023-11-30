import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Box, Button, Card, CardContent, IconButton, Input, Modal, Switch, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import { apiRequest } from '../../assets/_commons';

function ToDoModal(task, openModal, closeModal, methods, newTask) {
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const student_id = useSelector((state) => state.student.info.id);
  const dispatch = useDispatch();

  const [formData, setFormData] = useState({
    student_id: student_id,
    name: '',
    due_date: '',
    description: '',
    status: 'on_going'
  })

  useEffect(() => {
    if (task) {
      setFormData({
        student_id: student_id,
        name: task.name || '',
        due_date: task.due_date || '',
        description: task.description || '',
        status: task.status || ''
      });
    } else {
      // Reset formData if there's no task
      setFormData({ student_id: student_id, name: '', due_date: '', description: '', status: 'on_going' });
    }
  }, [task, newTask]);

  useEffect(_ => {
    setIsNew(newTask);
    setEdit(newTask);
  }, [newTask])

  const handleChange = (field, value) => {
    if (field === 'status') {
      value = value ? 'complete' : 'on_going';
    } else if (field === 'due_date' && value) {
      value = dayjs(value).format('YYYY-MM-DD');
    }

    setFormData(prev => {
      return { ...prev, [field]: value };
    });
  };

  const checkChanged = _ => {
    return task && (
      formData.name !== task.name || 
      formData.description !== task.description || 
      formData.due_date !== task.due_date ||  
      formData.status !== task.status
      )
  }

  const checkValid = _ => {
    return (
      formData.name.length > 0 &&
      formData.description.length > 0 &&
      formData.due_date.length > 0 &&
      (formData.status == 'on_going' || formData.status == 'complete')
    )
  }

  const getDifferentValues = _ => {
    if(task == null) return {}
    var body = {}
    if(formData.name !== task.name) body.name = formData.name
    if(formData.description !== task.description) body.description = formData.description
    if(formData.due_date !== task.due_date) body.end_date = formData.due_date
    if(formData.status !== task.status) body.type = formData.status
    return body
  }

  if (task == null && !isNew) { return null; }

  return (
    <Modal open={openModal || isNew} onClose={_ => {closeModal(); setEdit(false); setIsNew(false)}}>
      <Box style={{ width: '50%', height: '50%', backgroundColor: 'white', margin: '12.5% 25%', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black' }}>
        <div style={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem' }}>
          {edit ? (
            <TextField
              label="Name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              margin="normal"
              fullWidth
            />
          ) : (
            <h1 style={{ margin: '0' }}>{task ? task.name : ''}</h1>
          )}
          <div style={{ display: 'flex' }}>
            <IconButton onClick={_ => (isNew ? checkValid() ? setConfirmDelete(true) : closeModal() : setEdit(!edit))}>
              <EditIcon sx={{ color: '#630031' }} />
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <DeleteIcon sx={{ color: '#630031' }} />
            </IconButton>
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-around', paddingRight: '.75rem' }}>
          <Typography style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
            <b style={{ marginRight: '0.25rem' }}>Due Date:</b>
            {edit ? (
              <DatePicker
                value={formData.due_date.length > 0 ? dayjs(formData.due_date) : null}
                onChange={(newDate) => handleChange('due_date', newDate)}
              />
            ) : (
              formData.due_date || 'mm/dd/yyyy'
            )}
          </Typography>
          <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
            <Switch
              checked={formData.status === 'complete'}
              onChange={(e) => handleChange('status', e.target.checked)}
              disabled={!edit}
            />
            <Typography>Completed</Typography>
          </div>
        </div>
        <h3 style={{ margin: '0.25rem 0' }}>Description:</h3>
        {edit ? (
          <TextField
            label="Description"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            margin="normal"
            fullWidth
            multiline
            rows={4}
          />
        ) : (
          <Typography>{formData.description || 'No description provided.'}</Typography>
        )}
        <div style={{ position: 'absolute', left: '1rem', bottom: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <h3 style={{ display: 'inline-block', margin: '0.5rem 0' }}> Files: </h3>
            <Button component='label' startIcon={<FileUploadIcon sx={{ color: '#630031' }} />}>
              <Input type='file' style={{ width: '0' }} onChange={e => console.log(e.target.files)} />
            </Button>
          </div>
          <div style={{ height: '2rem', width: 'fit-content', border: '1px solid lightgray', borderRadius: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 1rem' }}>
            <h3 style={{ margin: '0' }}>File1.pdf</h3>
          </div>
        </div>
        {edit && (
          <Button
            style={{ position: 'absolute', right: '1rem', bottom: '1rem' }}
            variant='outlined'
            onClick={_ => {
              if(isNew){
                var body = {...formData};
                apiRequest(`student/event`, 'POST', body)
                .then(res => {
                  if(res.ok) return res.json();
                  else console.log(res.status);
                })
                .then(data => {
                  if (data == undefined) console.error('Error: Non ok http response');
                  else{
                      dispatch({type: 'add_task', payload: data})
                  }
                })
                .catch((err) => console.error('Error:', err.message))
              }
              else{ 
                apiRequest(`student/event/${task.id}`, 'PUT', getDifferentValues())
                .then(res => {
                  if(res.ok) return res.json();
                  else console.log(res.status);
                })
                .then(data => {
                  if (data == undefined) console.error('Error: Non ok http response');
                  else{
                      dispatch({type: 'update_task', payload: {id: task.id, data}})
                  }
                })
                .catch((err) => console.error('Error:', err.message))
              }
              setIsNew(false)
              setEdit(false)
              closeModal()
            }} 
            disabled={(!checkChanged() || isNew) && !checkValid()}>Save</Button>
        )}
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)}>
          <Box style={{ width: '13.5%', backgroundColor: 'white', margin: '12.5% auto', padding: '1rem', display: 'flex', flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' }}>
            <Typography variant="h6">Are you sure you want to delete this event?</Typography>
            <Button variant='outlined' style={{ marginRight: '1rem' }} onClick={_ => { if (!isNew) { methods.removeTask(task.id); } setConfirmDelete(false); closeModal(); }}>
              Confirm
            </Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>
              Cancel
            </Button>
          </Box>
        </Modal>
      </Box>
    </Modal>
  );
}

export default function ToDoList() {

  const [makeNew, setMakeNew] = useState(false);
  const [modal, setModal] = useState(null);

  const tasks = useSelector(state => state.student.tasks)
  const dispatch = useDispatch()

  const handleDelete = (event_id) => {
    fetch(`https://bktp-gradpro-api2.discovery.cs.vt.edu/student/event/${event_id}`, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(res => {
      if(res.ok) return res.json();
      else console.log(res.status);
    })
    .then(data => {
      if (data == undefined) console.error('Error: Non ok http response');
      else{
        dispatch({type: 'delete_task', payload: {id: event_id}})
      }
    })
    .catch((err) => console.error('Error:', err.message))
  }

  var closeModal = _ => {
    setModal(null)
    setMakeNew(false)
  }

  var makeTaskCards = _ => {
    const sortedTasks = tasks.sort((a, b) => {
      const dateA = new Date(a.due_date);
      const dateB = new Date(b.due_date);
      return dateA-dateB;
    });

    return sortedTasks.map(task => {
      const isPastDue = new Date(task.due_date) < new Date();
      const dueDateStyle = {
        marginBottom: '0',
        color: isPastDue ? 'red' : 'inherit'
      }
      return (
        <Card raised sx={{ marginX: '0.5rem' }} onClick={_ => { setModal(task); setMakeNew(false) }} key={`task-${task.id}`}>
          <CardContent style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'left', width: '10rem', height: '10rem', paddingBottom: '1.5rem' }}>
            <h1 style={{ margin: '0' }}>{task.name}</h1>
            <p>{task.description}</p>
            <p style={dueDateStyle}><b>Due:</b> {task.due_date}</p>
          </CardContent>
        </Card>
      )
    })
  }

  return (
    <>
      <Card className="to-do-list-container" sx={{ backgroundColor: '#F0F0F0' }}>
        <CardContent sx={{ padding: '8px 16px' }}>
          <Typography variant="h6" component="div" sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <strong>To Do List</strong>
            <IconButton onClick={_ => setMakeNew(true)}>
              <AddCircleOutlineIcon sx={{ color: '#630031' }} />
            </IconButton>
          </Typography>
          {/* Placeholder box, uses the to-do-list-placeholder class for styling */}
          <div style={{ overflowX: 'scroll' }}>
            <div className="to-do-list-placeholder">
              {makeTaskCards()}
            </div>
          </div>
        </CardContent>
      </Card>
      {ToDoModal(modal, modal !== null, closeModal, { removeTask: handleDelete }, makeNew)}
    </>
  );
}
