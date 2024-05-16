import React from 'react';
import {Box, CircularProgress, Typography} from "@mui/material";


interface CircularProgressProps {
    percentage: number;
}

export const ProgressWithPercent = (props: CircularProgressProps) => {
    return (
        <Box sx={{position: 'relative', display: 'inline-flex'}}>
            <CircularProgress variant="determinate" {...props} value={props.percentage} />
            <Box
                sx={{
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    position: 'absolute',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Typography
                    variant="caption"
                    component="div"
                    color="text.secondary"
                >{`${Math.round(props.percentage)}%`}</Typography>
            </Box>
        </Box>
    );
};

