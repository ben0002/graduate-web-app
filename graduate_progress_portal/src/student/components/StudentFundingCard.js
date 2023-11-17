import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';

const StudentFundingCard = () => {

  return (
    <Card className="student-funding-card-container">
      <CardContent>
        <Typography variant="h6" component="div">
          <strong>Student Funding</strong>
        </Typography>
        <div className="student-funding-card-placeholder">
          <Typography variant="body1">No funding yet</Typography>
        </div>
      </CardContent>
    </Card>
  );
};

export default StudentFundingCard;
