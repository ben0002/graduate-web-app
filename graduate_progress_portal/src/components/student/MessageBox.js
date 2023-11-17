import React from 'react';
import { Box, Tab, Tabs, TextField, Button, Paper } from '@mui/material';

const MessageBox = () => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <Paper sx={{ padding: '1em', margin: 'auto' }}>
      <Tabs value={value} onChange={handleChange} aria-label="message tabs">
        <Tab label="Message Student" />
        <Tab label="Private Admin Notes" />
      </Tabs>
      <Box
        component="form"
        sx={{
          '& .MuiTextField-root': { m: 1, width: 'stretch' },
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
        />
        <Button variant="contained" sx={{ marginTop: '1em' }}>
          Submit
        </Button>
      </Box>
    </Paper>
  );
}

export default MessageBox;
