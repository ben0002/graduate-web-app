import React, { useEffect, useState } from 'react';
import { Box, Button, Card, CardContent, Checkbox, FormControlLabel, IconButton, MenuItem, Modal, Select, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import { useDispatch, useSelector } from 'react-redux';
import { apiRequest, isNumeric, terms } from '../../assets/_commons';
import { DatePicker } from '@mui/x-date-pickers';
import dayjs from 'dayjs';
//import './StudentCourseHistoryCard.css';

function CourseModal(openModal, setOpen){
    const [localValues, setLocalValues] = useState({course_title: '', term: 0, year: 0, credits: 0, course_type: 'Non-Transfer'});
    const student_id = useSelector(state => state.student.info.id)
    const dispatch = useDispatch();

    useEffect(_=>{
      setLocalValues({course_title: '', term: 0, year: 0, credits: 0, course_type: 'Non-Transfer'})
    }, [openModal])
  
    const checkValid = _ => {
      return (
        localValues.course_title.length > 0 &&
        localValues.term >= 0 &&
        localValues.year >= 0 &&
        localValues.credits >= 0 &&
        localValues.course_type != null
      )
    }
  
    const handleInputChange = (name, value) => {
      setLocalValues({...localValues, [name]: value})
    }
  
    return(
    <Modal open={openModal} onClose={_ => {console.log(1); setOpen(false)}} style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{backgroundColor: 'white', padding: '1rem', position: 'relative', borderRadius: '0.5rem', boxShadow: '0px 0px 15px 0 black'}}>
          <div style={{borderBottom: '2px solid gray', borderRadius: '0.25rem', marginBottom: '0.5rem'}}>
            <h1 style={{margin: '0'}}>Add Course</h1>
          </div>
          <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-between', columnGap: '1rem', marginBottom: '3rem'}}>
            <TextField
                label="Course Title"
                value={localValues.course_title}
                onChange={(e) => handleInputChange('course_title', e.target.value)}
                variant="outlined"
            />
            <Select
                value={localValues.term}
                label="Term"
                onChange={(e) => {if(isNumeric(e.target.value)) handleInputChange('term', +e.target.value)}}
                sx={{width: '7rem'}}
            >
                <MenuItem value="0">Fall</MenuItem>
                <MenuItem value="1">Winter</MenuItem>
                <MenuItem value="2">Spring</MenuItem>
                <MenuItem value="3">Summer</MenuItem>
            </Select>
            <DatePicker
                    label="Year"
                    views={['year']}
                    value={localValues.year.length > 0 ? dayjs(localValues.year) : null}
                    onChange={(e) => handleInputChange('year', dayjs(e).format("YYYY"))}
                />
            <TextField
                label="Credits"
                value={localValues.credits}
                onChange={(e) => {if(isNumeric(e.target.value)) handleInputChange('credits', +e.target.value)}}
                type="number"
                variant="outlined"
            />
            <FormControlLabel control={
                <Checkbox
                    checked={localValues.course_type == 'Transfer'}
                    onChange={(e) => handleInputChange('course_type', e.target.checked ? 'Transfer' : 'Non-Transfer')}
                />} 
                label="Transfer" 
            /> 
          </div>
          <Button style={{position: 'absolute', right: '1rem', bottom: '1rem'}} variant='outlined' 
            onClick={_ => {
                var body = {...localValues};
                body.student_id = student_id
                body.pos_id = 1 //state.student.pos.id
                apiRequest(`student/course`, 'POST', body)
                .then(res => {
                    if(res.ok) return res.json();
                    else console.log(res.status);
                })
                .then(data => {
                    if (data == undefined) console.error('Error: Non ok http response');
                    else{
                        console.log(data)
                        dispatch({type: 'add_course', payload: data})
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

export default function StudentCourseHistoryCard() {

    const [confirmDelete, setConfirmDelete] = useState(null);
    const [open, setOpen] = useState(false);
    const courses = useSelector(state => state.student.courses)
    const dispatch = useDispatch()

    var makeCourseRows = _ => {
        return courses.map( (course, idx) => { return(
            <TableRow style={{backgroundColor: `${idx % 2 === 0 ? '#f5f5f5' : 'white'}`}}  key={`course-${course.id}`}>
                <TableCell align='center'>{course.course_title}</TableCell>
                <TableCell align='center'>{terms[course.term]}</TableCell>
                <TableCell align='center'>{course.year}</TableCell>
                <TableCell align='center'>{course.credits}</TableCell>
                <TableCell align='center'><Checkbox disabled checked={course.course_type == 'Transfer'}/></TableCell>
                <TableCell align='center'><Checkbox disabled/></TableCell>
                <TableCell align='center'><IconButton onClick={_ => setConfirmDelete(course.id)}><HighlightOffIcon/></IconButton></TableCell>
            </TableRow>
        )
        })
    }

    return (<>
        <Card className="student-course-history-container">
            <CardContent>
                <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <strong>Course History</strong>
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
                                    <TableCell align='center'>Course Name</TableCell>
                                    <TableCell align='center'>Term</TableCell>
                                    <TableCell align='center'>Year</TableCell>
                                    <TableCell align='center'>Credits</TableCell>
                                    <TableCell align='center'>Transfer</TableCell>
                                    <TableCell align='center'>Research/Dissertation</TableCell>
                                    <TableCell align='center'>Delete</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {makeCourseRows()}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </CardContent>
        </Card>
        {CourseModal(open, setOpen)}
        <Modal open={confirmDelete != null} onClose={_ => setConfirmDelete(null)} style={{display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <div style={{backgroundColor: 'white', padding: '1rem', display: 'flex', flexDirection: 'column', flexWrap: 'wrap', justifyContent: 'space-between', alignItems: 'center'}}>
              <h2 style={{marginTop: '0'}}>Are you sure you want to delete this event?</h2>
              <div>
                <Button variant='outlined' style={{marginRight: '1rem'}}
                    onClick={_ => {
                    apiRequest(`student/course/${confirmDelete}`, 'DELETE', null)
                    .then(res => {
                        if(res.ok) return res.json();
                        else console.log(res.status);
                    })
                    .then(data => {
                        if (data == undefined) console.error('Error: Non ok http response');
                        else{
                        dispatch({type: 'delete_course', payload: {id: confirmDelete}})
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
