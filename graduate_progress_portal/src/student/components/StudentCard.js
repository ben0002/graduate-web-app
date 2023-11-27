import React, { useState } from 'react';
import { Tooltip, Button, Card, CardContent, Typography, Avatar, Box, Grid } from '@mui/material';
import { Link, useLocation, useParams } from 'react-router-dom';
import { useFetchStudent } from '../StudentEffects';

import './StudentCard.css';

const StudentCardInfo = ({ student_id }) => {
    console.log("StudentCardInfo: student_id = ", student_id);

    const [student, setStudent] = useState({ role: 'student' });
    const [program, setProgram] = useState(null);
    const [advisor, setAdvisor] = useState(null);
  

    const defaultAvatar = '/path/to/default/avatar.jpg';

    useFetchStudent(student_id, setStudent, setAdvisor, setProgram);

    const location = useLocation();

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
                                <Typography variant="h6" component="div">
                                    <strong>
                                        {/* If the student has a middle name, display it. Otherwise, left out */}
                                        {student.first_name} {student.middle_name && `${student.middle_name} `}{student.last_name}
                                    </strong>
                                </Typography>
                                <Typography fontSize={13} color="textSecondary">{student.pronouns}</Typography>
                                <br />
                                <Typography color="textSecondary">
                                    <strong>Advisor:</strong> {advisor ? `${advisor.first_name} ${advisor.last_name}` : 'N/A'}
                                </Typography>
                                <Tooltip title={student.committee || 'N/A'}>
                                    <Typography
                                        className="truncate"
                                        fontSize={13}
                                        color="textSecondary"
                                        style={{ maxWidth: '27%' }} // Truncate everything after 27% of the container width
                                    >
                                        <strong>Committee: </strong>{student.advisory_committee || 'N/A'}
                                    </Typography>
                                </Tooltip>
                            </Box>
                        </Box>
                    </Grid>

                    {/* Column 2: Major, Status, Year */}
                    <Grid item xs={12} sm={2}>
                        <Box sx={{ flexGrow: 1 }}>
                            <Typography color="textSecondary"><strong>Major: </strong>{program?.major?.name || 'N/A'}</Typography>
                            <Typography color="textSecondary"><strong>Status: </strong>{student.type}</Typography>
                            <Typography color="textSecondary"><strong>Year: </strong></Typography>
                        </Box>
                    </Grid>

                    {/* Column 3: Concentration, Degree Type */}
                    <Grid item xs={12} sm={2}>
                        <Box sx={{ flexGrow: 1 }}>
                            <Typography color="textSecondary"><strong>Concentration: </strong></Typography>
                            <Typography color="textSecondary"><strong>Degree Type: </strong>{program?.degree?.name}</Typography>
                        </Box>
                    </Grid>

                    {/* Column 4: Action Buttons */}
                    <Grid item xs={12} sm={3}>
                        <Box display="flex" flexDirection="column" alignItems="center">
                            <Button
                                variant="contained"
                                sx={{
                                    backgroundColor: "#630031",
                                    '&:hover': { backgroundColor: '#4E342E' }
                                }}
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

export default StudentCardInfo;
