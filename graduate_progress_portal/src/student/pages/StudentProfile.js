import React from 'react';
import { Typography, Grid, Card, Divider, Box } from '@mui/material';
import { Link } from 'react-router-dom'
import { studentData } from '../SampleStudentData';
import StudentCardInfo from '../components/StudentCard';

const StudentProfile = () => {
    return (
        <Box sx={{ width: '65%', mx: 'auto' }}> {/* Adjust this width for the global container */}
            <Grid container spacing={2}>
                {/* Student Card */}
                <Grid item xs={12}>
                    <StudentCardInfo student={studentData} />
                </Grid>
            </Grid>
        </Box>
    );
}

export default StudentProfile;