import React from 'react';
import {Backdrop, CircularProgress} from '@mui/material';

export interface BackdropLoaderProps {
    open: boolean;
    onClick: () => void;
}

export const BackdropLoader: React.FC<BackdropLoaderProps> = ({open, onClick}) => (
    <Backdrop
        sx={{color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}}
        open={open}
        onClick={onClick}
    >
        <CircularProgress color="inherit"/>
    </Backdrop>
);