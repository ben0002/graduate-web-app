import React from 'react';
import { Card, CardContent, Typography, TextField, Button, Grid } from '@mui/material';

const StudentLabInformationCard = () => {
    return (
        <Card variant="outlined">
            <CardContent>
                <Grid container spacing={2} alignItems="center" justifyContent="space-between">
                    <Grid item xs={3}>
                        <Typography variant="subtitle1" gutterBottom>Labs</Typography>
                    </Grid>
                    <Grid item xs={3}>
                        <Typography variant="subtitle1" gutterBottom>Start Date</Typography>
                    </Grid>
                    <Grid item xs={3}>
                        <Typography variant="subtitle1" gutterBottom>Lab Head</Typography>
                    </Grid>
                    <Grid item xs={3}>
                        <Typography variant="subtitle1" gutterBottom>Location</Typography>
                    </Grid>
                </Grid>
                <Grid container spacing={2} alignItems="center">
                    <Grid item xs={3}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Lab Name"
                        />
                    </Grid>
                    <Grid item xs={3}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="YYYY-MM-DD"
                        />
                    </Grid>
                    <Grid item xs={3}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Head's Name"
                        />
                    </Grid>
                    <Grid item xs={3}>
                        <TextField
                            fullWidth
                            variant="outlined"
                            placeholder="Lab Location"
                        />
                    </Grid>
                    <Grid item xs={12} sx={{display: 'flex', justifyContent:'center'}}>
                        <Button variant="contained" sx={{
                            marginTop: 2, backgroundColor: "#630031", borderRadius: 20,
                        }}>Add</Button>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
    );
};

export default StudentLabInformationCard;
