import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import './StudentEmploymentCard.css';

const StudentEmploymentCard = () => {
  
  return (
    <Card className="student-employment-card-container">
      <CardContent>
        <Typography variant="h6" component="div">
          <strong>Student Employment</strong>
        </Typography>
        <div className="student-employment-card-placeholder">
          <Typography variant="body1">No employment yet</Typography>
        </div>
      </CardContent>
    </Card>
  );
};

export default StudentEmploymentCard;
