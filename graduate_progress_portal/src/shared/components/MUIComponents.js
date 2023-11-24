import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MenuItem, Menu, Typography, Box, Tab, Tabs, TextField, Button, Paper, Avatar, useLocation } from '@mui/material';

const UserAvatar = ({ studentData, onClick }) => {
    return (
        <Avatar
            alt={studentData.name}
            src={studentData.avatar}
            onClick={onClick}
        />
    );
};

const UserRole = ({ studentData }) => {
    return (
        <Typography variant="subtitle1">{studentData.userRole}</Typography>
    );
};

const MessageDisplay = () => {
    return (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="subtitle1">Message</Typography>
        </Box>
    );
};

const CustomButton = () => {
    return (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="subtitle1">Button</Typography>
        </Box>
    );
}

export { UserAvatar, UserRole, MessageDisplay, CustomButton };


