import React from 'react';
import {Paper, PaperProps, useTheme} from '@mui/material';

interface PaperContainerProps extends PaperProps {
    children: React.ReactNode;
}

export const PaperContainerComponent: React.FC<PaperContainerProps> = ({children, ...otherProps}) => {
    const theme = useTheme();
    return (
        <Paper
            sx={{
                width: '80%',
                height: "90vh",
                overflow: 'hidden',
                position: 'left',
                marginTop: '10vh',
                backgroundColor: theme.palette.secondary.light
            }}
        >
            {children}
        </Paper>
    );
};

