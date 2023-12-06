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
import '../../assets/styling/student/studentToDoListCard';

function ToDoModal(task, openModal, closeModal, newTask) {
  const [isNew, setIsNew] = useState(false);
  const [edit, setEdit] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);
  const student_id = useSelector((state) => state.student.info.id);
  const dispatch = useDispatch();

  const [formData, setFormData] = useState({
    name: '',
    due_date: '',
    description: '',
    status: 'on_going'
  })

  useEffect(() => {
    if (task) {
      setFormData({
        name: task.name || '',
        due_date: task.due_date || '',
        description: task.description || '',
        status: task.status || ''
      });
    } else {
      // Reset formData if there's no task
      setFormData({ name: '', due_date: '', description: '', status: 'on_going' });
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

    setFormData({ ...formData, [field]: value })
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
      formData.due_date.length > 0 &&
      (formData.status == 'on_going' || formData.status == 'complete')
    )
  }

  const getDifferentValues = _ => {
    if(task == null) return {}
    var body = {}
    if(formData.name !== task.name) body.name = formData.name
    if(formData.description !== task.description) body.description = formData.description
    if(formData.due_date !== task.due_date) body.due_date = formData.due_date
    if(formData.status !== task.status) body.type = formData.status
    return body
  }

  if (task == null && !isNew) { return null; }

  return (
    <Modal open={openModal || isNew} onClose={_ => {closeModal(); setEdit(false); setIsNew(false)}} className='flex flexCenter'>
      <div className='modalBox'>
        <div className='flex modalHeader'>
          {edit ? (
            <TextField
              label="Name"
              value={formData.name}
              onChange={(e) => handleChange('name', e.target.value)}
              margin="normal"
              fullWidth
            />
          ) : (
            <h1>{task ? task.name : ''}</h1>
          )}
          <div className='flex'>
            <IconButton onClick={_ => (isNew ? checkValid() ? setConfirmDelete(true) : closeModal() : setEdit(!edit))}>
              <EditIcon sx={{ color: '#630031' }} />
            </IconButton>
            <IconButton onClick={_ => setConfirmDelete(true)}>
              <DeleteIcon sx={{ color: '#630031' }} />
            </IconButton>
          </div>
        </div>
        <div className='flex flexCenter modalBody'>
          <Typography className='flex flexCenter'>
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
          <div className='flex flexCenter'>
            <Switch
              checked={formData.status === 'complete'}
              onChange={(e) => handleChange('status', e.target.checked)}
              disabled={!edit}
            />
            <Typography>Completed</Typography>
          </div>
        </div>
        <h3 className='toDoModalDescription'>Description:</h3>
        {edit ? (
          <TextField
            label="Description"
            value={formData.description}
            onChange={(e) => handleChange('description', e.target.value)}
            margin="normal"
            fullWidth
            multiline
            rows={6}
          />
        ) : (
          <Typography>{formData.description || 'No description provided.'}</Typography>
        )}
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
        {edit && (
          <Button
            className='saveButton actionButton'
            variant='outlined'
            onClick={_ => {
              if(isNew){
                var body = {...formData};
                apiRequest(`students/${student_id}/events`, 'POST', body)
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
                apiRequest(`student/${student_id}/events/${task.id}`, 'PATCH', getDifferentValues())
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
        <Modal open={confirmDelete} onClose={_ => setConfirmDelete(false)} className='flex flexCenter'>
        <div className="flex flexColumn flexWrap flexCenter modalBox">
            <Typography variant="h6">Are you sure you want to delete this event?</Typography>
            <Button variant='outlined' style={{ marginRight: '1rem' }} 
            onClick={_ => { if (!isNew) { 
              apiRequest(`students/${student_id}/events/${task.id}`, 'DELETE', null)
              .then(res => {
                if(res.ok) return res.json();
                else console.log(res.status);
              })
              .then(data => {
                if (data == undefined) console.error('Error: Non ok http response');
                else{
                  dispatch({type: 'delete_task', payload: {id: task.id}})
                }
              })
              .catch((err) => console.error('Error:', err.message))
            } setConfirmDelete(false); closeModal(); }}>
              Confirm
            </Button>
            <Button variant='outlined' onClick={_ => setConfirmDelete(false)}>
              Cancel
            </Button>
          </div>
        </Modal>
      </div>
    </Modal>
  );
}

export default function ToDoList() {

  const [makeNew, setMakeNew] = useState(false);
  const [modal, setModal] = useState(null);

  const tasks = useSelector(state => state.student.tasks)

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
      return (
        <Card raised sx={{ marginX: '0.5rem' }} onClick={_ => { setModal(task); setMakeNew(false) }} key={`task-${task.id}`}>
          <CardContent className='flex flexColumn taskCardItem'>
            <h1>{task.name}</h1>
            <p>{task.description}</p>
            <p className={isPastDue ? 'dueDatePast' : 'dueDateFuture'}><b>Due:</b> {task.due_date}</p>
          </CardContent>
        </Card>
      )
    })
  }

  return (
    <>
      <Card className="toDoListContainer">
        <CardContent sx={{ padding: '8px 16px' }}>
          <Typography variant="h6" component="div" className='flex'>
            <strong>To Do List</strong>
            <IconButton onClick={_ => setMakeNew(true)}>
              <AddCircleOutlineIcon sx={{ color: '#630031' }} />
            </IconButton>
          </Typography>
          {/* Placeholder box, uses the to-do-list-placeholder class for styling */}
          <div className='overflowX'>
            <div className="flex flexCenter toDoList">
              {makeTaskCards()}
            </div>
          </div>
        </CardContent>
      </Card>
      {ToDoModal(modal, modal !== null, closeModal, makeNew)}
    </>
  );
}
