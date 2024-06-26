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

// const StudentProgress = () => {
//   return (
//     <Box sx={{ width: '65%', mx: 'auto' }}> {/* Adjust this width for the global container */}
//       {/* Margin for cards */}
//       <Grid container spacing={2}>
//         {/* StudentCard and StudentProfileCard */}
//         <Grid item xs={12}>
//           <StudentCardInfo student={studentData} />
//         </Grid>
//         <Grid item xs={12}>
//           <ToDoList student={studentData.tasks} />
//         </Grid>

//         {/* Milestones */}
//         <Grid item xs={12} md={5}>
//           <StudentMilestoneCard student={studentData.milestones} />
//         </Grid>

//         {/* Requirements */}
//         <Grid item xs={12} md={5}>
//           <StudentRequirementCard student={studentData.requirements} />
//         </Grid>

//         {/* Funding and Employment with Divider */}
//         <Grid item xs={12} md={2} sx={{ display: 'flex', flexDirection: 'column' }}>
//           <StudentFundingCard student={studentData.funding} />
//           <Divider />
//           <StudentEmploymentCard student={studentData.employment} />
//         </Grid>

//         {/* Course History */}
//         <Grid item xs={10}>
//           <StudentCourseHistoryCard student={studentData.courseHistory} />
//         </Grid>

//       </Grid>
//     </Box>
//   );
// };

const StudentProgress = () => {
  return (
    <Box sx={{ width: '65%', mx: 'auto' }}> {/* Adjust this width for the global container */}
      {/* Margin for cards */}
      <Grid container spacing={2}>
        {/* StudentCard and StudentProfileCard */}
        <Grid item xs={12}>
          <StudentCardInfo student={studentData} />
        </Grid>
        <Grid item xs={12}>
          <ToDoList student={studentData.tasks} />
        </Grid>
        <Grid container item spacing={2}>
          <Grid item xs={10}>
            <Grid container spacing={2}>
              {/* Milestones */}
              <Grid item xs={6}>
                <StudentMilestoneCard />
              </Grid>
              {/* Requirements */}
              <Grid item xs={6}>
                <StudentRequirementCard />
              </Grid>
              {/* Course History */}
              <Grid item xs={12}>
                <StudentCourseHistoryCard/>
              </Grid>
            </Grid>
          </Grid>
          {/* Funding and Employment */}
          <Grid item xs={2}>
            <Grid container direction="column" spacing={2}>
              {/* Funding */}
              <Grid item>
                <StudentFundingCard />
              </Grid>
              {/* Divider */}
              <Divider orientation="horizontal" flexItem />
              {/* Employment */}
              <Grid item>
                <StudentEmploymentCard/>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
}
export default StudentProgress;
