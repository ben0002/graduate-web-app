import React, { useState, useEffect } from 'react';
import { Box, TextField, Button, Paper, Typography, Modal, MenuItem, FormControl, Select, Grid, IconButton } from '@mui/material';
import { apiRequest } from '../../assets/_commons';
import { useSelector } from 'react-redux';
import '../../assets/styling/student/studentAdvisorCommitteeCard';


const StudentAdvisorCommittee = () => {
  const [advisors, setAdvisors] = useState([]);
  const [committeeMembers, setCommitteeMembers] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [newMember, setNewMember] = useState({ name: '', role: '', advisorType: '' });
  const student_id = useSelector(state => state.student.info.id)

  const handleOpenModal = () => {
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setNewMember({ name: '', role: '', advisorType: '' });
  };

  const handleInputChange = (e) => {
    setNewMember({ ...newMember, [e.target.name]: e.target.value });
  };

  useEffect(() => {
    // Fetch advisors
    apiRequest(`students/${student_id}/advisors`, 'GET')
      .then(response => response.json())
      .then(data => setAdvisors(data))
      .catch(error => console.error('Error fetching advisors:', error));

    // Fetch committee members
    apiRequest(`students/${student_id}`, 'GET')
      .then(response => response.json())
      .then(data => setCommitteeMembers(data.advisory_committee.split(',')))
      .catch(error => console.error('Error fetching committee members:', error));
  }, [student_id]);

  const displayAdvisorInfo = (advisorRole) => {
    const advisorArray = advisors.filter(a => a.advisor_role === advisorRole);
    if (advisorArray.length > 0) {
      const advisor = advisorArray[0];
      return (
        <>
          <Typography className='advisorName'>{`${advisor.first_name} ${advisor.last_name}`}</Typography>
          <Typography className='advisorInfo'>{`Email: ${advisor.email}`}</Typography>
          <Typography className='advisorInfo'>{`Department: ${advisor.dept_code}`}</Typography>
          <Typography className='advisorInfo'>{`Faculty-Type: ${advisor.faculty_type}` || ''}</Typography>
        </>
      );
    }
    return <Typography className='advisorName'>Not Assigned</Typography>;
  };

  return (
    <Paper>
      <Box className='studentAdvisorCommitteeContainer'>
        <Grid container spacing={2}>
          {/* Left Side - Advisor */}
          <Grid item xs={6}>
            <Typography variant="h6" className='advisorTitle'>Advisors</Typography>
            <Typography className='advisor'>Main Advisor:</Typography>
            {displayAdvisorInfo('main_advisor')}
            <Typography className='advisor coAdvisor'>Co-Advisor:</Typography>
            {displayAdvisorInfo('co_advisor')}
          </Grid>

          {/* Right Side - Committee */}
          <Grid item xs={6}>
            <Typography variant="h6" className='committeeTitle'>Committee</Typography>
            {committeeMembers.length > 0 ? committeeMembers.map((member, index) => (
              <Typography key={index} className='committeeMember'>{member}</Typography>
            )) : <Typography className='committeeMember'>Not assigned</Typography>}
          </Grid>
        </Grid>

        <Button onClick={handleOpenModal} className='addButton'>Add Member</Button>

        {/* Modal for adding member */}
        <Modal open={modalOpen} onClose={handleCloseModal}>
          <Box className='ACmodalBox'>
            <TextField fullWidth label="Name" name="name" value={newMember.name} disabled margin="normal" />
            <FormControl fullWidth margin="normal">
              <Select name="role" value={newMember.role} disabled displayEmpty>
                <MenuItem value="" disabled>Select Role</MenuItem>
                <MenuItem value="advisor">Advisor</MenuItem>
                <MenuItem value="committee">Committee</MenuItem>
              </Select>
            </FormControl>
            {newMember.role === 'advisor' && (
              <FormControl fullWidth margin="normal">
                <Select name="advisorType" value={newMember.advisorType} disabled displayEmpty>
                  <MenuItem value=""  >Select Advisor Type</MenuItem>
                  <MenuItem value="Main Advisor">Main Advisor</MenuItem>
                  <MenuItem value="Co-Advisor">Co-Advisor</MenuItem>
                </Select>
              </FormControl>
            )}
            <Button disabled className='addButton'>Add</Button>
          </Box>
        </Modal>
      </Box>
    </Paper>
  );
};

export default StudentAdvisorCommittee;
