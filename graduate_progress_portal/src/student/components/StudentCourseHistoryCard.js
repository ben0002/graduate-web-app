import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import './StudentCourseHistoryCard.css';

const StudentCourseHistoryCard = () => {
    return (
        <Card className="student-course-history-container">
            <CardContent>
                <Typography variant="h6" component="div">
                    <strong>Course History</strong>
                </Typography>
                {/* Placeholder box, uses the milestones-placeholder class for styling */}
                <div className="student-course-history-placeholder">
                    <Typography variant="body1">No courses yet</Typography>
                </div>
            </CardContent>
        </Card>
    );
}

export default StudentCourseHistoryCard;