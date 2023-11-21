import React from 'react';
import { Box, Grid, Card, Divider } from '@mui/material';
import { studentData } from '../SampleStudentData';
import StudentCardInfo from '../components/StudentCard';
import StudentPersonalCardInfo from '../components/StudentPersonalInfoCard';
import MessageBox from '../components/MessageBox';
import StudentAdvisorCommitteeCard from '../components/StudentAdvisorCommitteeCard';
import StudentLabInformationCard from '../components/StudentLabsCard.js';
import StudentCourseHistoryCard from '../components/StudentCourseHistoryCard';

const StudentProfile = () => {
    return (
        <Box sx={{ width: '65%', mx: 'auto', my: 4 }}> {/* Adjust this width for the global container */}
            <Grid container justifyContent="center" alignItems="flex-start" spacing={2}>
                <Grid item xs={12}>
                    <Card>
                        <StudentCardInfo student={studentData} />
                        <Divider variant="middle" />
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
                        <Box sx={{maxHeight: '19rem', overflowY: 'auto'}}>
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
