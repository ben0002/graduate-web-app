import React, { useState } from 'react';
import { Card, CardContent, IconButton, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
//import './StudentRequirementCard.css';

var count = 2;

export default function StudentRequirementCard() {

    const [requirements, setRequirements] = useState([{Name: "First", id: 1}]);

    var addRequirement = _ => {
        setRequirements(requirements.concat({Name: `${count}`, id: count}))
        count += 1;
    }

    var removeRequirement = id => {
        setRequirements(requirements.filter( requirement => requirement.id != id))
    }

    var makeRequirementCards = _ => {
        return requirements.map( requirement => { return(
            <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
                <h2 style={{margin: '0'}}>{requirement.Name}</h2>
                <IconButton onClick={_ => removeRequirement(requirement.id)}>
                    <HighlightOffIcon sx={{color: '#630031'}}/>
                </IconButton>
            </div>
        )
        })
    }

    return (
        <Card className="student-requirements-container">
            <CardContent>
                <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <strong>Requirements</strong>
                    <IconButton onClick={ _ => addRequirement()}>
                        <AddCircleOutlineIcon sx={{color: '#630031'}}/>
                    </IconButton>
                </Typography>
            {/* Placeholder box, uses the requirements-placeholder class for styling */}
            <div style={{overflowY: 'scroll', overflowX: 'hidden'}}>
                    <div className="student-requirements-placeholder">
                        {makeRequirementCards()}
                    </div>
                </div>
        </CardContent>
        </Card>
    );
}