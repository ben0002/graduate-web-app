import React from 'react';

import { Grid, Card, Divider, Box } from '@mui/material';
import { studentData } from '../../assets/data/SampleStudentData.jsx';
import StudentCardInfo from '../../components/student/StudentCard.js';
import ToDoList from '../../components/student/StudentToDoListCard.js';
import StudentMilestoneCard from '../../components/student/StudentMilestoneCard.js';
import StudentRequirementCard from '../../components/student/StudentRequirementCard.js';
import StudentFundingCard from '../../components/student/StudentFundingCard.js'; 
import StudentEmploymentCard from '../../components/student/StudentEmploymentCard.js'; 
import StudentCourseHistoryCard from '../../components/student/StudentCourseHistoryCard.js';

const StudentProgress = () => {
  return (
    <Box sx={{ width: '70%', paddingX: '2.5%', mx: 'auto', backgroundColor: '#f2f2f2', marginTop: '1rem', paddingBottom: '1rem'}}>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <StudentCardInfo student={studentData} />
        </Grid>
        <Grid item xs={12}>
          <ToDoList student={studentData.tasks} />
        </Grid>
        <Grid container item spacing={2}>
          <Grid item xs={10}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <StudentMilestoneCard />
              </Grid>
              <Grid item xs={6}>
                <StudentRequirementCard />
              </Grid>
              <Grid item xs={12}>
                <StudentCourseHistoryCard />
              </Grid>
            </Grid>
          </Grid>
          <Grid item xs={2}>
            <Grid container direction="column" spacing={2}>
              <Grid item>
                <StudentFundingCard />
              </Grid>
              <Divider orientation="horizontal" flexItem />
              <Grid item>
                <StudentEmploymentCard />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
}
export default StudentProgress;
