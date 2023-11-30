import React from 'react';
import { Tooltip, Button, Card, CardContent, Typography, Avatar, Box, Grid } from '@mui/material';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';


export default function StudentCardInfo() {
    const defaultAvatar = '/path/to/default/avatar.jpg'; // Replace with some sort of endpoint later?

    const location = useLocation();
    const navigate = useNavigate();

    const user = useSelector(state => state.student)

    const getMainAdvisor = _ => {
        var main_adv = user.advisors.filter(adv => adv.role == "main_advisor")
        if(main_adv.length > 0) return main_adv[0].name
        return null
    }

    if(user == undefined) return (<></>)
    
    return (
        <Card className="student-card-container" sx={{ height: '165px' }}>
            <CardContent>
                <Grid container spacing={2} alignItems="flex-start">
                    {/* Column 1: Avatar and basic info */}
                    <Grid item xs={12} sm={5}>
                        <Box display="flex" alignItems="flex-start">
                            <Avatar
                                alt={`${user.info.first_name || 'First'} ${user.info.middle_name || ''} ${user.info.last_name || 'Last'} Name`}
                                src={defaultAvatar}
                                sx={{ width: 56, height: 56, marginRight: 2 }}
                            />
                            <Box sx={{ flexGrow: 1 }}>
                                <Typography variant="h6" component="div"><strong>{`${user.info.first_name || 'First'} ${user.info.middle_name || ''} ${user.info.last_name || 'Last'}`}</strong></Typography>
                                <Typography fontSize={13} color="textSecondary">{user.info.pronoun || 'N/A'}</Typography>
                                <br />
                                <Typography color="textSecondary"><strong>Advisor:</strong> {getMainAdvisor() || 'N/A'}</Typography>
                                <Tooltip title={user.info.advisory_committee || 'N/A'}>
                                    <Typography 
                                        className="truncate" 
                                        fontSize={13} 
                                        color="textSecondary"
                                        style={{ maxWidth: '27%' }} // Truncate everything after 27% of the container width
                                    >
                                        <strong>Committee: </strong>{user.info.advisory_committee || 'N/A'}
                                    </Typography>
                                </Tooltip>
                            </Box>
                        </Box>
                    </Grid>

                    {/* Column 2: Major, Status, Year */}
                    <Grid item xs={12} sm={2}>
                        <Box sx={{ flexGrow: 1 }}>
                            <Typography color="textSecondary"><strong>Major: </strong>{user.programs.length > 0 ? user.programs[0].major : 'Major'}</Typography> {/*user.programs.map( pro => pro.major).join(', ')*/}
                            <Typography color="textSecondary"><strong>Status: </strong>{user.info.status || 'New'}</Typography>
                            <Typography color="textSecondary"><strong>Year: </strong>{user.info.year || 2023}</Typography>
                        </Box>
                    </Grid>

                    {/* Column 3: Concentration, Degree Type */}
                    <Grid item xs={12} sm={2}>
                        <Box sx={{ flexGrow: 1 }}>
                            <Typography color="textSecondary"><strong>Concentration: </strong>{user.info.concentration || 'Concentration'}</Typography>
                            <Typography color="textSecondary"><strong>Degree Type: </strong>{user.programs.length > 0 ? user.programs[0].degree : 'Degree'}</Typography> {/*user.programs.map( pro => pro.degree).join(', ')*/}
                        </Box>
                    </Grid>

                    {/* Column 4: Action Buttons */}
                    <Grid item xs={12} sm={3}>
                        <Box display="flex" flexDirection="column" alignItems="center">
                            <Button
                                variant="contained"
                                //color="primary"
                                sx = {{backgroundColor: "#630031"}}
                                component={Link}
                                to={location.pathname.includes('/student/profile') ? "/student/progress" : "/student/profile"}
                                >
                                {location.pathname.includes('/student/profile') ? "Go to Progress" : "Go to Profile"}
                            </Button>
                            <Button
                                variant="contained"
                                color="secondary"
                                sx={{ mt: 2 }} 
                                onClick={() => { /* Logic to print PDF */ }}
                                disabled={true}
                            >
                                Print PDF
                            </Button>
                        </Box>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};
