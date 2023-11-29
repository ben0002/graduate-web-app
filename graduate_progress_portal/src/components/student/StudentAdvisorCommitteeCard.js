import React, { useState } from 'react';
import { Box, TextField, Button, Paper, Typography } from '@mui/material';

const StudentAdvisorCommittee = () => {
  const [advisors, setAdvisors] = useState([]);
  const [committeeMembers, setCommitteeMembers] = useState([]);
  const [newAdvisor, setNewAdvisor] = useState('');
  const [newCommitteeMember, setNewCommitteeMember] = useState('');

  const handleAddAdvisor = (event) => {
    event.preventDefault();
    if (newAdvisor.trim()) {
      setAdvisors([...advisors, newAdvisor.trim().toUpperCase()]);
      setNewAdvisor('');
    }
  };

  const handleAddCommitteeMember = (event) => {
    event.preventDefault();
    if (newCommitteeMember.trim()) {
      setCommitteeMembers([...committeeMembers, newCommitteeMember.trim().toUpperCase()]);
      setNewCommitteeMember('');
    }
  };

  return (
    <Paper>
      <Box sx={{ display: 'flex', flexDirection: 'column', p: 2 }}>
        {/* Advisor Section */}
        <Box sx={{ flex: 1, borderBottom: '1px solid black', mb: 2, paddingBottom: "0.5rem" }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#630031', mb: 1 }}>Advisor(s)</Typography>
          {advisors.map((advisor, index) => (
            <Typography key={index} sx={{ fontSize: 12 }}>{advisor}</Typography>
          ))}
          <form onSubmit={handleAddAdvisor} style={{ display: 'flex', alignItems: 'center' }}>
            <TextField 
              value={newAdvisor}
              onChange={(e) => setNewAdvisor(e.target.value)}
              size="medium"
              placeholder="Enter Advisor Name"
              InputProps={{
                disableUnderline: true,
                sx: {
                  fontSize: 16,
                  '&::placeholder': {
                    color: 'rgba(0, 0, 0, 0.6)'
                  }
                }
              }}
              sx={{ flexGrow: 1, mr: 1 }}
            />
            <Button
              type="submit"
              sx={{
                backgroundColor: '#630031', 
                color: 'white',
                borderRadius: 20,
                '&:hover': {
                  backgroundColor: '#4E342E'
                },
                p: '6px 16px',
              }}
            >
              Add
            </Button>
          </form>
        </Box>
        
        {/* Committee Section */}
        <Box sx={{ flex: 1, borderBottom: '1px solid black', paddingBottom: "0.5rem" }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold', color: '#630031', mb: 1 }}>Committee</Typography>
          {committeeMembers.map((member, index) => (
            <Typography key={index} sx={{ fontSize: 12 }}>{member}</Typography>
          ))}
          <form onSubmit={handleAddCommitteeMember} style={{ display: 'flex', alignItems: 'center' }}>
            <TextField 
              value={newCommitteeMember}
              onChange={(e) => setNewCommitteeMember(e.target.value)}
              size="medium"
              placeholder="Enter Committee Member Name"
              InputProps={{
                disableUnderline: true,
                sx: {
                  fontSize: 16,
                  '&::placeholder': {
                    color: 'rgba(0, 0, 0, 0.6)'
                  }
                }
              }}
              sx={{ flexGrow: 1, mr: 1 }}
            />
            <Button
              type="submit"
              sx={{
                backgroundColor: '#630031',
                color: 'white',
                borderRadius: 20,
                '&:hover': {
                  backgroundColor: '#4E342E'
                },
                p: '6px 16px',
              }}
            >
              Add
            </Button>
          </form>
        </Box>
      </Box>
    </Paper>
  );
};

export default StudentAdvisorCommittee;
