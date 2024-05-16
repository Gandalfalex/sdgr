import React from 'react';
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import {SnackbarSeverity} from "../../../typedefs/error_types";

interface CustomSnackbarProps {
    open: boolean;
    onClose: () => void;
    duration?: number;
    severity?: SnackbarSeverity; // Add more if needed
    message?: string;
}

const CustomSnackbar: React.FC<CustomSnackbarProps> = ({
                                                           open,
                                                           onClose,
                                                           duration = 6000,
                                                           severity = SnackbarSeverity.ERROR,
                                                           message = 'An error occurred!',
                                                       }) => {
    return (
        <Snackbar
            open={open}
            autoHideDuration={duration}
            onClose={onClose}
            anchorOrigin={{vertical: 'bottom', horizontal: 'left'}}
        >
            <Alert severity={severity} sx={{width: '100%'}}>
                {message}
            </Alert>
        </Snackbar>
    );
};

export default CustomSnackbar;