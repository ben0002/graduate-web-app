import React, { useState } from 'react';
import { Card, CardContent, IconButton, Typography } from '@mui/material';
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

    var makeCourseCards = _ => {
        return courses.map( course => { return(
            <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
                <h2 style={{margin: '0'}}>{course.Name}</h2>
                <IconButton onClick={_ => removeCourse(course.id)}>
                    <HighlightOffIcon sx={{color: '#630031'}}/>
                </IconButton>
            </div>
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
                <div style={{overflowY: 'scroll', overflowX: 'hidden'}}>
                    <div className="student-course-history-placeholder">
                        {makeCourseCards()}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
