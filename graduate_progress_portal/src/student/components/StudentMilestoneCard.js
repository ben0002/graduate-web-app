import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import './StudentMilestoneCard.css';

const StudentMilestoneCard = () => {
    return (
        <Card className="student-milestones-container">
            <CardContent>
                <Typography variant="h6" component="div">
                    <strong>Milestones</strong>
                </Typography>
                <div className="student-milestones-placeholder">
                    <Typography variant="body1">No milestones yet</Typography>
                </div>
            </CardContent>
        </Card>
    );
}

export default StudentMilestoneCard;
