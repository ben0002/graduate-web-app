import React, { useState } from 'react';
import { Tooltip, Button, Card, CardContent, Typography, Avatar, Box, Grid } from '@mui/material';
import './StudentPersonalInfoCard.css';
import { useFetchStudent } from '../StudentEffects';

const StudentPersonalCardInfo = ({ student_id }) => {
    const [student, setStudent] = useState({ role: 'student' });
    useFetchStudent(student_id, setStudent);

    return (
        <Card className="student-personal-info-container">
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
                            {student.phone_number}
                        </Typography>
                        <Typography variant="body1" component={'div'}>
                            <strong>Residence: </strong>{student.va_residency}
                            {student.va_residency === 'Out-of-State' ?  (
                                <Typography variant="body1" component={'div'}>
                                    <strong>Country: </strong>{student.citizenship || 'N/A'}
                                </Typography>
                            ) : null}
                        </Typography>
                    </Grid>
                    <Grid item xs={12} sm={4}>
                        {/* Column 2: Program Entry, Admit Camp */}
                        <Typography
                            variant='body1'
                            component='div'>
                            <strong>Program Entry: </strong>
                            {student.first_term}
                        </Typography>
                        <Typography
                            variant='body1'
                            component='div'>
                            <strong>Campus: </strong>
                            {student.campus_id}
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