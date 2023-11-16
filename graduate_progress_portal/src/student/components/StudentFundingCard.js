import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const StudentFundingCard = () => {
  return (
    <Card className="student-funding-card-container">
      <CardContent>
        <Typography variant="h6" component="div">
          <strong>Student Funding</strong>
        </Typography>
        {/* Content related to student funding goes here */}
      </CardContent>
    </Card>
  );
};

export default StudentFundingCard;
