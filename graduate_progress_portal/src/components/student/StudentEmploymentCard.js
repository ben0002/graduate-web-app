import React, { useState } from 'react';
import { Card, CardContent, IconButton, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
//import './StudentEmploymentCard.css';

var count = 2;

export default function StudentEmploymentCard() {

  const [employments, setEmployments] = useState([{Name: "First", id: 1}]);

  var addEmployment = _ => {
    setEmployments(employments.concat({Name: `${count}`, id: count}))
    count += 1;
  }

  var removeEmployment = id => {
    setEmployments(employments.filter( employment => employment.id != id))
  }

  var makeEmploymentCards = _ => {
    return employments.map( employment => { return(
      <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
        <h2 style={{margin: '0'}}>{employment.Name}</h2>
        <IconButton onClick={_ => removeEmployment(employment.id)}>
          <HighlightOffIcon sx={{color: '#630031'}}/>
        </IconButton>
      </div>
    )})
  }

  return (
    <Card className="student-employment-card-container">
      <CardContent>
        <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
          <strong>Student Employment</strong>
          <IconButton onClick={ _ => addEmployment()}>
            <AddCircleOutlineIcon sx={{color: '#630031'}}/>
          </IconButton>
        </Typography>
        {/* Content related to student employment goes here */}
        <div style={{overflowY: 'scroll', overflowX: 'hidden', minHeight: '25rem', maxHeight: '25rem'}}>
          <div className="student-employment-card-placeholder">
            {makeEmploymentCards()}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};
