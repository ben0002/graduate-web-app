import React from 'react';
import { Grid, Card, Divider, Box } from '@mui/material';
import { studentData } from '../SampleStudentData.jsx';
import StudentCardInfo from '../components/StudentCard';
import ToDoList from '../components/ToDoBox.js';
import StudentMilestoneCard from '../components/StudentMilestoneCard.js';
import StudentRequirementCard from '../components/StudentRequirementCard.js';
import StudentFundingCard from '../components/StudentFundingCard.js'; 
import StudentEmploymentCard from '../components/StudentEmploymentCard.js'; 
import StudentCourseHistoryCard from '../components/StudentCourseHistoryCard.js';

const StudentProgress = () => {
  return (
    <Box sx={{ width: '65%', mx: 'auto' }}> {/* Adjust this width for the global container */}
      <Grid container spacing={2}>
        {/* Student Card */}
        <Grid item xs={12}>
          <StudentCardInfo student={studentData} />
        </Grid>
        {/* Student To Do List */}
        <Grid item xs={12}>
          <ToDoList student={studentData.tasks} />
        </Grid>

        {/* Second row for Milestones, Requirements, and combined Funding/Employment */}
        <Grid container item xs={12} spacing={2}> 
          <Grid item xs={12} md={5} lg={5}>
            <StudentMilestoneCard student={studentData.milestones} />
          </Grid>
          <Grid item xs={12} md={5} lg={5}>
            <StudentRequirementCard student={studentData.requirements} />
          </Grid>
          {/*  Funding and Employment Card*/}
          <Grid item xs={12} md={2} lg={2}>
            <Card raised sx={{ display: 'flex', flexDirection: 'column', height: '200%' }}>
              <Box sx={{ display: 'flex', flexDirection: 'column', flexGrow: 1 }}>
                <Box sx={{ flex: 1 }}>
                  <StudentFundingCard student={studentData.funding} />
                </Box>
                <Box sx={{ flex: 0.9}}>
                  <StudentEmploymentCard student={studentData.employment} />
                </Box>
              </Box>
            </Card>
          </Grid>
          {/*  Student Course History Card */}
          <Grid item xs={12} md={10} lg={10}>
            <StudentCourseHistoryCard student={studentData.courseHistory} />
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StudentProgress;
