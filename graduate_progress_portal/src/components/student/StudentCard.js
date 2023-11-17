import React from 'react';
import { Tooltip, Button, Card, CardContent, Typography, Avatar, Box, Grid } from '@mui/material';
import { Link } from 'react-router-dom';
//import '../../assets/styling/student/';

export default function StudentCardInfo({ student }) {
    const defaultAvatar = '/path/to/default/avatar.jpg'; // Replace with some sort of endpoint later?

    return (
        <Card className="student-card-container" sx={{ height: '165px' }}>
            <CardContent>
                <Grid container spacing={2} alignItems="flex-start">
                    {/* Column 1: Avatar and basic info */}
                    <Grid item xs={12} sm={5}>
                        <Box display="flex" alignItems="flex-start">
                            <Avatar
                                alt={student.name}
                                src={student.image || defaultAvatar}
                                sx={{ width: 56, height: 56, marginRight: 2 }}
                            />
                            <Box sx={{ flexGrow: 1 }}>
                                <Typography variant="h6" component="div"><strong>{student.name}</strong></Typography>
                                <Typography fontSize={13} color="textSecondary">{student.pronoun}</Typography>
                                <br />
                                <Typography color="textSecondary"><strong>Advisor:</strong> {student.advisor || 'N/A'}</Typography>
                                <Tooltip title={student.committee || 'N/A'}>
                                    <Typography 
                                        className="truncate" 
                                        fontSize={13} 
                                        color="textSecondary"
                                        style={{ maxWidth: '27%' }} // Truncate everything after 27% of the container width
                                    >
                                        <strong>Committee: </strong>{student.committee || 'N/A'}
                                    </Typography>
                                </Tooltip>
                            </Box>
                        </Box>
                    </Grid>

                    {/* Column 2: Major, Status, Year */}
                    <Grid item xs={12} sm={2}>
                        <Box sx={{ flexGrow: 1 }}>
                            <Typography color="textSecondary"><strong>Major: </strong>{student.major}</Typography>
                            <Typography color="textSecondary"><strong>Status: </strong>{student.status}</Typography>
                            <Typography color="textSecondary"><strong>Year: </strong>{student.year}</Typography>
                        </Box>
                    </Grid>

                    {/* Column 3: Concentration, Degree Type */}
                    <Grid item xs={12} sm={2}>
                        <Box sx={{ flexGrow: 1 }}>
                            <Typography color="textSecondary"><strong>Concentration: </strong>{student.concentration}</Typography>
                            <Typography color="textSecondary"><strong>Degree Type: </strong>{student.degreeType}</Typography>
                        </Box>
                    </Grid>

                    {/* Column 4: Action Buttons */}
                    <Grid item xs={12} sm={3}>
                        <Box display="flex" flexDirection="column" alignItems="center">
                            <Button
                                variant="contained"
                                color="primary"
                                component={Link}
                                to="/student/profile"
                            >
                                Profile
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
