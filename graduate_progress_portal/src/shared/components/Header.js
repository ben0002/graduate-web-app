import React, { useState } from 'react';
import { AppBar, Toolbar, Box, Badge, Avatar } from '@mui/material';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { UserAvatar, UserRole } from './MUIComponents';
import DropDownMenu from './DropDownMenu';
import { studentData } from '../../student/SampleStudentData.jsx';
import logoSrc from '../../assets/images/VTLogo.png';

const Header = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleAvatarClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static" style={{
      backgroundColor: '#630031',
      height: '4rem',
      borderBottom: '.2rem solid #E5751F'
    }}>
      <Toolbar style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '100%' }}>
        <UserRole studentData={studentData} />

        <img src={logoSrc} alt="Logo" style={{ maxHeight: '3rem' }} />

        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Badge badgeContent={4} color="secondary" sx={{ marginRight: '1rem' }}>
            <NotificationsIcon />
          </Badge>
          <Box onClick={handleAvatarClick} sx={{ cursor: 'pointer' }}>
            <UserAvatar studentData={studentData} />
          </Box>
          <DropDownMenu
            anchorEl={anchorEl}
            open={open}
            onClose={handleClose}
            userRole={studentData.userRole}
          />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;