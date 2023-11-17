import React from 'react';
import { Card, CardContent, Typography, TextField, Button, Grid } from '@mui/material';

const StudentAdvisorCommitteeCard = () => {
    return (
        <Card variant="outlined" sx={{ minHeight: '300px' }}> {/* Adjust minHeight as necessary */}
            <CardContent>
                <Typography variant="h6">Advisor(s)</Typography>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={9}>
                        <TextField
                            fullWidth
                            placeholder="Enter advisor's name"
                            variant="outlined"
                        />
                    </Grid>
                    <Grid item xs={3}>
                        <Button variant="contained">Add</Button>
                    </Grid>
                </Grid>
                <Typography variant="h6" sx={{ marginTop: 2 }}>Committee</Typography>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={9}>
                        <TextField
                            fullWidth
                            placeholder="Enter committee member's name"
                            variant="outlined"
                        />
                    </Grid>
                    <Grid item xs={3}>
                        <Button variant="contained">Add</Button>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
}

export default StudentAdvisorCommitteeCard;
