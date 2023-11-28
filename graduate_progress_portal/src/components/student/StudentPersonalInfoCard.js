import React from 'react';
import { Tooltip, Button, Card, CardContent, Typography, Avatar, Box, Grid } from '@mui/material';
//import './StudentPersonalInfoCard.css';

const StudentPersonalCardInfo = ({ student }) => {
    return (
        <Card className="student-personal-info-container" sx={{backgroundColor: '#F0F0F0', border: '.3rem solid #75787b'}}>
            <CardContent>
                <Grid container spacing={2} alignItems={'flex-start'}>
                    <Grid item xs={12} sm={4}>
                        <Box sx={{ flexGrow: 1 }}>
                            </Box>
                    {/* Column 1: Email, Phone, Ethnicity, Country/Residence */}
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Email: </strong>
                                {student.email}
                        </Typography>
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Phone: </strong>
                                {student.phone}
                        </Typography>
                        <Typography
                            variant='body1'
                            component={'div'}>
                                <strong>Ethnicity: </strong>
                                {student.ethnicity}
                        </Typography>
                        <Typography
                            variant='body1'
                            component={'div'}>
                                <strong>Country/Residence: </strong>
                                {student.ethnicity}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                    {/* Column 2: Program Entry, Admit Camp */}
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Program Entry: </strong>
                                {student.programEntry}
                        </Typography>
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>Admit Camp: </strong>
                                {student.admitCamp}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                    {/* Column 3: POS, posOnFile */}
                        <Typography 
                            variant='body1' 
                            component='div'>
                                <strong>POS: </strong>
                                {student.planOfStudy}
                        </Typography>
                        {/** Add in logic to check if the status of POS */}
                    </Grid>
                </Grid> 
            </CardContent>
        </Card>
    );
}

export default StudentPersonalCardInfo;