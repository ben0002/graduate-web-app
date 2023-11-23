import React, { useState } from 'react';
import { Card, CardContent, Checkbox, IconButton, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
//import './StudentCourseHistoryCard.css';

var count = 2;

export default function StudentCourseHistoryCard() {

    const [courses, setCourses] = useState([{Name: "First", id: 1}]);

    var addCourse = _ => {
        setCourses(courses.concat({Name: `${count}`, id: count}))
        count += 1;
    }

    var removeCourse = id => {
        setCourses(courses.filter( course => course.id != id))
    }

    var makeCourseRows = _ => {
        return courses.map( (course, idx) => { return(
            <TableRow style={{backgroundColor: `${idx % 2 ? '#f5f5f5' : 'white'}`}}>
                <TableCell align='center'>{course.id}</TableCell>
                <TableCell align='center'>{course.Name}</TableCell>
                <TableCell align='center'>spring {course.id}</TableCell>
                <TableCell align='center'>{2000 + course.id}</TableCell>
                <TableCell align='center'>3</TableCell>
                <TableCell align='center'><Checkbox/></TableCell>
                <TableCell align='center'><Checkbox/></TableCell>
            </TableRow>
        )
        })
    }

    return (
        <Card className="student-course-history-container">
            <CardContent>
                <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <strong>Course History</strong>
                    <IconButton onClick={ _ => addCourse()}>
                        <AddCircleOutlineIcon sx={{color: '#630031'}}/>
                    </IconButton>
                </Typography>
                {/* Placeholder box, uses the milestones-placeholder class for styling */}
                <div style={{overflowX: 'hidden', height: '18rem'}}>
                    <TableContainer sx={{maxHeight: '18rem'}}>
                        <Table stickyHeader aria-label="sticky table">
                            <TableHead>
                                <TableRow>
                                    <TableCell align='center'>Course ID</TableCell>
                                    <TableCell align='center'>Course Name</TableCell>
                                    <TableCell align='center'>Term</TableCell>
                                    <TableCell align='center'>Year</TableCell>
                                    <TableCell align='center'>Credits</TableCell>
                                    <TableCell align='center'>Transfer</TableCell>
                                    <TableCell align='center'>Research/Dissertation</TableCell>
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
    );
}
