import React, { useEffect, useState } from 'react';
import { Box, Button, Card, CardContent, IconButton, Modal, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import DeleteIcon from '@mui/icons-material/Delete';
import { useDispatch, useSelector } from 'react-redux';
import { apiGetRequest, apiRequest } from '../../assets/_commons';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
import '../../assets/styling/student/studentLabCard';

function LabModal(openModal, setOpen){
    const [localValues, setLocalValues] = useState({name: '', start_date: '', director: '', location: ''});
    const student_id = useSelector(state => state.student.info.id)
    const dispatch = useDispatch();

    useEffect(_=>{
      setLocalValues({name: '', start_date: '', director: '', location: ''})
    }, [openModal])
  
    const checkValid = _ => {
      return (
        localValues.name.length > 0 &&
        localValues.start_date.length > 0 &&
        localValues.director.length > 0 &&
        localValues.location.length > 0
      )
    }
  
    const handleInputChange = (name, value) => {
      setLocalValues({...localValues, [name]: value})
    }
  
    return(
    <Modal open={openModal} onClose={_ => {console.log(1); setOpen(false)}} className='flex flexCenter'>
          <div className='modalBox'>
            <div className='modalHeader'>
              <h1>Add Lab</h1>
            </div>
            <div className='flex modalLabForm'>
                <TextField
                    label="Lab Name"
                    value={localValues.name}
                    onChange={(e) => handleInputChange('name', e.target.value)}
                    variant="outlined"
                />
                <DatePicker
                    label="Start Date"
                    value={localValues.start_date.length > 0 ? dayjs(localValues.start_date) : null}
                    onChange={(e) => handleInputChange('start_date', dayjs(e).format("YYYY-MM-DD"))}
                />
                <TextField
                    label="Director"
                    value={localValues.director}
                    onChange={(e) => handleInputChange('director', e.target.value)}
                    variant="outlined"
                />
                <TextField
                    label="Location"
                    value={localValues.location}
                    onChange={(e) => handleInputChange('location', e.target.value)}
                    variant="outlined"
                />
                
            </div>
            <Button className='saveButton actionButton' variant='outlined' 
                onClick={_ => {
                    var body = {...localValues};
                    apiRequest(`students/${student_id}/labs`, 'POST', body, true)
                    .then(res => {
                        if(res.ok) return res.json();
                        else console.log(res.status);
                    })
                    .then(data => {
                        if (data == undefined) console.error('Error: Non ok http response');
                        else{
                            console.log(data)
                            dispatch({type: 'add_lab', payload: data})
                            setOpen(false)
                        }
                    })
                    .catch((err) => console.error('Error:', err.message))
                }} 
                disabled={!checkValid()}
            >
                Save
            </Button>
          </div>
    </Modal>
    )
}

const StudentLabInformationCard = () => {
    const [confirmDelete, setConfirmDelete] = useState(null);
    const [open, setOpen] = useState(false);
    const labs = useSelector(state => state.student.labs)
    const dispatch = useDispatch()
    const student_id = useSelector(state => state.student.info.id)
    
    useEffect(_ => { 
        apiGetRequest(`students/${student_id}/labs`, 'GET', null)  
        .then(res => {
            if(res.ok) return res.json();
            else console.log(res.status);
        })
        .then(data => {
            if (data == undefined) console.error('Error: Non ok http response');
            else{
                console.log(data)
                dispatch({type: 'pop_stu_labs', payload: data});
            }
        })
        .catch((err) => console.error('Error:', err.message))     
      }, []);

    var makeLabRows = _ => {
        return labs.map( (lab, idx) => { return(
                <TableRow className={`${idx % 2 === 0 ? 'tableRowAlternate' : 'tableRow'}`}  key={`lab-${lab.id}`}>
                    <TableCell align='center'>{lab.name}</TableCell>
                    <TableCell align='center'>{lab.start_date}</TableCell>
                    <TableCell align='center'>{lab.director}</TableCell>
                    <TableCell align='center'>{lab.location}</TableCell>
                    <TableCell align='center'><IconButton onClick={_ => setConfirmDelete(lab.id)}><DeleteIcon/></IconButton></TableCell>
                </TableRow>
            )
            })
        }
    
    return (<>
        <Card className="studentLabContainer"> {/* does this actually provide any styling? */}
            <CardContent>
                <Typography variant="h6" component="div" className='flex'>
                    <strong>Labs</strong>
                    <IconButton onClick={ _ => setOpen(true)}>
                        <AddCircleOutlineIcon sx={{color: '#630031'}}/>
                    </IconButton>
                </Typography>
                <div className="studentLabList">
                    <TableContainer sx={{maxHeight: '18rem'}}>
                        <Table stickyHeader aria-label="sticky table">
                            <TableHead>
                                <TableRow>
                                    <TableCell align='center'>Lab Name</TableCell>
                                    <TableCell align='center'>Start Date</TableCell>
                                    <TableCell align='center'>Director</TableCell>
                                    <TableCell align='center'>Location</TableCell>
                                    <TableCell align='center'>Delete</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {makeLabRows()}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </CardContent>
        </Card>
        {LabModal(open, setOpen)}
        <Modal open={confirmDelete != null} onClose={_ => setConfirmDelete(null)} className='flex flexCenter'>
                <div className="flex flexColumn flexWrap flexCenter modalBox">
                    <h2>Are you sure you want to delete this event?</h2>
                    <div>
                        <Button variant='outlined' style={{marginRight: '1rem'}}
                            onClick={_ => {
                            apiRequest(`${student_id}/labs/${confirmDelete}`, 'DELETE', null, true)
                            .then(res => {
                                if(res.ok) return res.json();
                                else console.log(res.status);
                            })
                            .then(data => {
                                if (data == undefined) console.error('Error: Non ok http response');
                                else{
                                dispatch({type: 'delete_lab', payload: {id: confirmDelete}})
                                }
                            })
                            .catch((err) => console.error('Error:', err.message))
                            setConfirmDelete(null)}}
                        >
                            Confrim
                        </Button>
                        <Button variant='outlined' onClick={_ => setConfirmDelete(null)}>Keep Event</Button>
                    </div>
                </div>
        </Modal>
    </>);
}

export default StudentLabInformationCard;
