import React, { useEffect, useState } from 'react';
import { Box, Button, Card, CardContent, IconButton, Modal, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import { useDispatch, useSelector } from 'react-redux';
import { apiRequest } from '../../assets/_commons';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';

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
    <Modal open={openModal} onClose={_ => {console.log(1); setOpen(false)}} style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <div style={{backgroundColor: 'white', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
            <div style={{borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
              <h1 style={{margin: '0'}}>Add Lab</h1>
            </div>
            <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', columnGap: '1rem', marginBottom: '3rem'}}>
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
            <Button style={{position: 'absolute', right: '1rem', bottom: '1rem'}} variant='outlined' 
                onClick={_ => {
                    var body = {...localValues};
                    body.student_id = student_id
                    apiRequest(`student/lab`, 'POST', body)
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
    
    var makeLabRows = _ => {
        return labs.map( (lab, idx) => { return(
                <TableRow style={{backgroundColor: `${idx % 2 === 0 ? '#f5f5f5' : 'white'}`}}  key={`lab-${lab.id}`}>
                    <TableCell align='center'>{lab.name}</TableCell>
                    <TableCell align='center'>yyyy-mm-dd</TableCell>
                    <TableCell align='center'>{lab.director}</TableCell>
                    <TableCell align='center'>located here</TableCell>
                    <TableCell align='center'><IconButton onClick={_ => setConfirmDelete(lab.id)}><HighlightOffIcon/></IconButton></TableCell>
                </TableRow>
            )
            })
        }
    
    return (<>
        <Card className="student-labs-container">
            <CardContent>
                <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <strong>Labs</strong>
                    <IconButton onClick={ _ => setOpen(true)}>
                        <AddCircleOutlineIcon sx={{color: '#630031'}}/>
                    </IconButton>
                </Typography>
                {/* Placeholder box, uses the milestones-placeholder class for styling */}
                <div style={{overflowX: 'hidden', height: '18rem'}}>
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
        <Modal open={confirmDelete != null} onClose={_ => setConfirmDelete(null)} style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
                <div style={{backgroundColor: 'white', padding: '1rem', display: 'flex', flexDirection: 'column', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center'}}>
                    <h2 style={{marginTop: '0'}}>Are you sure you want to delete this event?</h2>
                    <div>
                        <Button variant='outlined' style={{marginRight: '1rem'}}
                            onClick={_ => {
                            apiRequest(`student/lab/${confirmDelete}`, 'DELETE', null)
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
