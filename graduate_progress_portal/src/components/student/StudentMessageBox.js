import React, { useEffect } from 'react';
import { Box, Tab, Tabs, TextField, Button, Paper } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { apiGetRequest, apiRequest } from '../../assets/_commons';
import '../../assets/styling/student/studentMessageBox';

const StudentMessageBox = () => {
  const [value, setValue] = React.useState(0); // Tab value
  const dispatch = useDispatch()
  const messages = useSelector(state => state.student.messages)
  const student_id = useSelector(state => state.student.info.id) 

  useEffect(_ => {
    apiGetRequest(`students/${student_id}/messages`, 'GET', null)  
    .then(res => {
      if(res.ok) return res.json();
      else console.log(res.status);
    })
    .then(data => {
      if (data == undefined) console.error('Error: Non ok http response');
      else{
        console.log(data)
        dispatch({type: 'pop_stu_messages', payload: data});
      }
    })
    .catch((err) => console.error('Error:', err.message))    
  }, []);

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
    <Paper className='flex flexColumn messageBoxContainer'>
      {/** Renders the tabs based on userRole **/}
      <Tabs value={value} onChange={handleChange} aria-label="message tabs" >
        {tabsToShow.map((label, index) => (
          <Tab key={index} label={label} className='messageTab' />
        ))}
      </Tabs>
      <div className='overflowY messageArea'>
        <div className='flex flexColumn messageAreaContainer'>
        {[1,2,3,4,5,6].map(msg => 
          <div className='messageItem'>
            <p className='messageTimestamp'>hh:mm - mm/dd/yyyy, name</p>
            <p className='messageText'>This it the message text. and here is some kind of ong text to hopefully see what this looks like on the page and see how well it wraps</p>
          </div>)}
        </div>
      </div>
      <div className='messageInputArea'>
        <TextField
          id="message-box"
          label="Type your message here"
          multiline
          rows={1}
          placeholder="Enter message..."
          variant="outlined"
          className='fullWidth'
        />
        <Button
          variant="contained"
          className='submitButton'
        >
          Submit
        </Button>
      </div>
    </Paper>
  );
}

export default MessageBox;