import React, { useEffect } from 'react';
import { Box, Grid, Card, Divider } from '@mui/material';
import { studentData } from '../../assets/data/SampleStudentData.jsx';
import StudentCardInfo from '../../components/student/StudentInfoCard.js';
import StudentPersonalCardInfo from '../../components/student/StudentPersonalInfoCard';
import MessageBox from '../../components/student/MessageBox';
import StudentAdvisorCommitteeCard from '../../components/student/StudentAdvisorCommitteeCard';
import StudentLabInformationCard from '../../components/student/StudentLabsCard';
import StudentCourseHistoryCard from '../../components/student/StudentCourseHistoryCard';
import { useDispatch } from 'react-redux';

const StudentProfile = () => {
    
    const dispatch = useDispatch();

    useEffect(_ => {
        async function profile() {
            await fetch("https://bktp-gradpro-api.discovery.cs.vt.edu/student/profile", {
                credentials: 'include', // To include cookies in the request
                headers: {
                    'Accept': 'application/json', // Explicitly tell the server that you want JSON
                }
            })
            .then(res => {
                if(res.ok) return res.json();
                else console.log(res.status);
            })
            .then(data => {
                if (data == undefined) console.error('Error: Non ok http response');
                else{
                    console.log(data)
                    dispatch({type: 'pop_stu_profile', payload: data});
                }
            })
            .catch((err) => console.error('Error:', err.message))    
        }
        profile();      
    }, []);

    return (
        <Box sx={{
            width: '70%',
            paddingX: '2.5%',
            mx: 'auto',
            my: 4,
            marginTop: '1rem',
            paddingBottom: '1rem'
        }}> {/* Adjust this width for the global container */}
            <Grid container justifyContent="center" alignItems="flex-start" spacing={2}>
                <Grid item xs={12}>
                    <Card>
                        <StudentCardInfo student={studentData} />
                    </Card>
                    <Divider />
                    <Card>
                        <StudentPersonalCardInfo student={studentData} />
                    </Card>
                </Grid>
            </Grid>
            <Grid container alignItems="flex-start" paddingTop="16px">
                <Grid item xs={12} md={7} lg={7} sx={{ pr: 2 }}>
                    <MessageBox />
                </Grid>
                <Grid item xs={12} md={5} lg={5}>
                    <Card>
                        <Box sx={{ maxHeight: '19rem', overflowY: 'auto' }}>
                            <StudentAdvisorCommitteeCard />
                        </Box>
                    </Card>
                </Grid>
            </Grid>
            <Grid container alignItems="flex-start" paddingTop="16px">
                <Grid item xs={12}>
                    <StudentLabInformationCard />
                </Grid>
            </Grid>
            <Grid container alignItems="flex-start" paddingTop="16px">
                <Grid item xs={12}>
                    <StudentCourseHistoryCard />
                </Grid>
            </Grid>
        </Box>
    );
}

export default StudentProfile;
