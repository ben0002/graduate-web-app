import React, { useState } from 'react';
import { Card, CardContent, IconButton, Typography } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
//import './StudentMilestoneCard.css';

var count = 2;

export default function  StudentMilestoneCard() {

    const [milestones, setMilestones] = useState([{Name: "First", id: 1}]);

    var addMilestone = _ => {
        setMilestones(milestones.concat({Name: `${count}`, id: count}))
        count += 1;
    }

    var removeMilestone = id => {
        setMilestones(milestones.filter( milestone => milestone.id != id))
    }

    var makeMilestoneCards = _ => {
        return milestones.map( milestone => { return(
            <div style={{ marginX: 'auto', width: '90%', position: 'relative', display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
                <h2 style={{margin: '0'}}>{milestone.Name}</h2>
                <IconButton onClick={_ => removeMilestone(milestone.id)}>
                    <HighlightOffIcon sx={{color: '#630031'}}/>
                </IconButton>
            </div>
        )
        })
    }

    return (
        <Card className="student-milestones-container">
            <CardContent>
                <Typography variant="h6" component="div" sx={{display: 'flex', justifyContent: 'space-between'}}>
                    <strong>Milestones</strong>
                    <IconButton onClick={ _ => addMilestone()}>
                        <AddCircleOutlineIcon sx={{color: '#630031'}}/>
                    </IconButton>
                </Typography>
                <div style={{overflowY: 'scroll', overflowX: 'hidden'}}>
                    <div className="student-milestones-placeholder">
                        {makeMilestoneCards()}
                    </div>
                </div>
            </CardContent>
        </Card>
    );
}
