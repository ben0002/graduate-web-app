import React from 'react';
import { Grid, Card, Divider, Box } from '@mui/material';
import { studentData } from '../../assets/data/SampleStudentData.jsx';
import StudentCardInfo from '../../components/student/StudentCard';
import ToDoList from '../../components/student/ToDoBox.js';
import StudentMilestoneCard from '../../components/student/StudentMilestoneCard.js';
import StudentRequirementCard from '../../components/student/StudentRequirementCard.js';
import StudentFundingCard from '../../components/student/StudentFundingCard.js'; 
import StudentEmploymentCard from '../../components/student/StudentEmploymentCard.js'; 
import StudentCourseHistoryCard from '../../components/student/StudentCourseHistoryCard.js';

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
          <Grid item xs={12} md={5} lg={5} sx={{height: 'fit-content'}}>
            <StudentMilestoneCard student={studentData.milestones} />
          </Grid>
          <Grid item xs={12} md={5} lg={5} sx={{height: 'fit-content'}}>
            <StudentRequirementCard student={studentData.requirements} />
          </Grid>
          {/*  Funding and Employment Card*/}
          <Grid item xs={12} md={2} lg={2}>
            <Card sx={{ display: 'flex', flexDirection: 'column', height: 'fit-content' }}>
                <Box sx={{ flex: 1 }}>
                  <StudentFundingCard student={studentData.funding} />
                </Box>
                <Box sx={{ flex: 0.9}}>
                  <StudentEmploymentCard student={studentData.employment} />
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
