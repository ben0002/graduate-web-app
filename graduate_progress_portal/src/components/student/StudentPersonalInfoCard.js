import React from 'react';
import { Tooltip, Button, Card, CardContent, Typography, Avatar, Box, Grid } from '@mui/material';
import { useSelector } from 'react-redux';
//import './StudentPersonalInfoCard.css';

const StudentPersonalCardInfo = ({ student }) => {

    const user = useSelector(state => state.student)

    return (
        <Card className="student-personal-info-container">
            <CardContent>
                <Grid container spacing={2} alignItems={'flex-start'}>
                    <Grid item xs={12} sm={4}>
                    {/* Column 1: Email, Phone, Ethnicity, Country/Residence */}
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Email: </strong>
                                {user.info.email || 'johndoe@vt.edu'}
                        </Typography>
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Phone: </strong>
                                {user.info.phone_number || '(123) 456-7890'}
                        </Typography>
                        <Typography
                            variant='body1'
                            component={'div'}>
                                <strong>Country/Residence: </strong>
                                {user.info.citizenship || 'citizenship'}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                    {/* Column 2: Program Entry, Admit Camp */}
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Program Entry: </strong>
                                {user.programs.length > 0 ? user.programs[0].enrollment_date : 'Enrolled'}
                        </Typography>
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Admit Camp: </strong>
                                {user.campus.name || 'campus'}, {user.campus.address || 'located here'}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                    {/* Column 3: POS, posOnFile */}
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>POS: </strong>
                                {user.POS_info || ''}
                        </Typography>
                        {/** Add in logic to check if the status of POS */}
                    </Grid>
                </Grid> 
            </CardContent>
        </Card>
    );
}

export default StudentPersonalCardInfo;