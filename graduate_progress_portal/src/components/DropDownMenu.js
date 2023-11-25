import { Menu, MenuItem } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import React from 'react';

const DropDownMenu = ({ anchorEl, open, onClose, userRole }) => {
    const navigate = useNavigate();

    {/* Items for Menu Items are declared here, based on UserRole
        Implement items changing based on user Location */}
    const menuItems = {
        // 'Admin': [
        // ],
        // 'Faculty': [
        // ],
        'Student': [
            { text: 'My Profile', path: '/student/profile' },
            { text: 'My Progress', path: '/student/progress' },
            { text: 'Logout', path: '/' },
        ]
    };

    const handleMenuItemClick = (path) => {
        navigate(path);
        onClose();
    };

    return (
        <Menu
            anchorEl={anchorEl}
            id="drop-down-menu"
            open={open}
            onClose={onClose}
            PaperProps={{
                elevation: 0,
                sx: {
                    overflow: 'visible',
                    filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                    mt: 1.5,
                    '& .MuiAvatar-root': {
                        width: 32,
                        height: 32,
                        ml: -0.5,
                        mr: 1,
                    },
                    '&:before': {
                        content: '""',
                        display: 'block',
                        position: 'absolute',
                        top: 0,
                        right: 14,
                        width: 10,
                        height: 10,
                        bgcolor: 'background.paper',
                        transform: 'translateY(-50%) rotate(45deg)',
                        zIndex: 0,
                    },
                },
            }}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
            {/*  Dynamically render menu options based on menuItems */}
            {menuItems[userRole] && menuItems[userRole].map((item) => (
                <MenuItem key={item.text} onClick={() => handleMenuItemClick(item.path)}>
                    {item.text}
                </MenuItem>
            ))}
        </Menu>
    );
}

export default DropDownMenu;