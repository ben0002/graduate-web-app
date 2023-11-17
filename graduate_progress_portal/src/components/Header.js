import React from 'react';
import { AppBar, Toolbar } from '@mui/material';

const Header = () => {
  const headerStyle = {
    backgroundColor: '#630031', // Chicago Maroon 
    height: '3rem',
    display: 'flex',
  };

  return (
    <AppBar position="static" style={headerStyle}>
      <Toolbar>
        {/* Components added here later */}
      </Toolbar>
    </AppBar>
  );
};

export default Header;
