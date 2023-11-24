import React from 'react';
import { Grid, Box, Divider } from '@mui/material';
import { studentData } from '../SampleStudentData.jsx';
import StudentCardInfo from '../components/StudentCard';
import ToDoList from '../components/StudentToDoListCard.js';
import StudentMilestoneCard from '../components/StudentMilestoneCard.js';
import StudentRequirementCard from '../components/StudentRequirementCard.js';
import StudentFundingCard from '../components/StudentFundingCard.js';
import StudentEmploymentCard from '../components/StudentEmploymentCard.js';
import StudentCourseHistoryCard from '../components/StudentCourseHistoryCard.js';

const StudentProgress = () => {
  return (
    <Box sx={{ width: '65%', mx: 'auto', mt: 4 }}>
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
