import React, { useEffect } from 'react';
import { Box, Grid, Card, Divider } from '@mui/material';
import { studentData } from '../../assets/data/SampleStudentData.jsx';
import StudentCardInfo from '../../components/student/StudentInfoCard.js';
import StudentPersonalCardInfo from '../../components/student/StudentPersonalInfoCard';
import StudentMessageBox from '../../components/student/StudentMessageBox';
import StudentAdvisorCommitteeCard from '../../components/student/StudentAdvisorCommitteeCard';
import StudentLabInformationCard from '../../components/student/StudentLabsCard';
import StudentCourseHistoryCard from '../../components/student/StudentCourseHistoryCard';

const StudentProfile = () => {

    return (
        <> {/* Adjust this width for the global container */}
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
        </>
    );
}

export default StudentProfile;
