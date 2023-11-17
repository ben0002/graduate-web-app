import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import './StudentFundingCard.css';

const StudentFundingCard = () => {

  return (
    <Card className="student-funding-card-container">
      <CardContent>
      <Typography variant="h6" component="div" sx={{ fontSize: theme => theme.typography.pxToRem(19) }}>
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
