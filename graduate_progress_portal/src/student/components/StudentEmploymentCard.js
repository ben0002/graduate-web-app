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
        {/* Content related to student employment goes here */}
      </CardContent>
    </Card>
  );
};

export default StudentEmploymentCard;
