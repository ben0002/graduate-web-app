import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import './StudentRequirementCard.css';

const StudentRequirementCard = () => {
    return (
        <Card className="student-requirements-container">
        <CardContent>
            <Typography variant="h6" component="div">
            <strong>Requirements</strong>
            </Typography>
            {/* Placeholder box, uses the milestones-placeholder class for styling */}
            <div className="student-requirements-placeholder">
            <Typography variant="body1">No requirements yet</Typography>
            </div>
        </CardContent>
        </Card>
    );
}

export default StudentRequirementCard;