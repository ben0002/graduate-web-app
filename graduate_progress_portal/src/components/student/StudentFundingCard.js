import React, { useState } from 'react';
import { Card, CardContent, IconButton, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';

var count = 2;

export default function StudentFundingCard() {

  const [fundings, setFundings] = useState([{Name: "First", id: 1}]);

  var addFunding = _ => {
    setFundings(fundings.concat({Name: `${count}`, id: count}))
    count += 1;
  }

  var removeFunding = id => {
    setFundings(fundings.filter( funding => funding.id != id))
  }

  var makeFundingCards = _ => {
    return fundings.map( funding => { return(
      <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
        <h2 style={{margin: '0'}}>{funding.Name}</h2>
        <IconButton onClick={_ => removeFunding(funding.id)}>
          <HighlightOffIcon sx={{color: '#630031'}}/>
        </IconButton>
      </div>
    )})
  }

  return (
    <Card className="student-funding-card-container">
      <CardContent>
        <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
          <strong>Student Funding</strong>
          <IconButton onClick={ _ => addFunding()}>
            <AddCircleOutlineIcon sx={{color: '#630031'}}/>
          </IconButton>
        </Typography>
        <div style={{overflowY: 'scroll', overflowX: 'hidden', minHeight: '17.5rem', maxHeight: '17.5rem'}}>
          <div className="student-funding-card-placeholder">
            {makeFundingCards()}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};