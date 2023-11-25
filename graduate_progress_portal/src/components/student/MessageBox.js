import React from 'react';
import { Box, Tab, Tabs, TextField, Button, Paper } from '@mui/material';

const MessageBox = () => {
  const [value, setValue] = React.useState(0); // Tab value 

  // Placeholder for future userRole check 
  const userRole = 'student'; // For testing purpose only. 'student' 'faculty' 'admin' 

  const handleChange = (event, newValue) => {
    setValue(newValue);
  }

  // Display tabs based on userRole
  const tabsByRole = {
    student: ["Message Advisor", "Private Student Notes"],
    faculty: ["Message Student", "Private Faculty Notes"],
    admin: ["Message User", "Private Admin Notes"]
  };

  const tabsToShow = tabsByRole[userRole] || [];

  return (
    <Paper sx={{ padding: '1em', margin: 'auto' }}>
      {/** Renders the tabs based on userRole */}
      <Tabs value={value} onChange={handleChange} aria-label="message tabs" >
        {tabsToShow.map((label, index) => (
          <Tab key={index} label={label} sx={{ color: '#630031', fontSize: "1rem" }} />
        ))}
      </Tabs>
      <Box
        component="form"
        sx={{
          '& .MuiTextField-root': { m: 1, width: '100%' },
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          padding: '1em'
        }}
        noValidate
        autoComplete="off"
      >
        <TextField
          id="message-box"
          label="Type your message here"
          multiline
          rows={4}
          placeholder="Enter message..."
          variant="outlined"
          fullWidth
        />
        <Box sx={{ width: '100%', display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
          <Button
            variant="contained"
            sx={{
              borderRadius: 20,
              backgroundColor: '#630031',
              color: 'white',
              '&:hover': {
                backgroundColor: '#4E342E'
              }
            }}
          >
            Submit
          </Button>
        </Box>
      </Box>
    </Paper>
  );
}

export default MessageBox;