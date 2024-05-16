import React, {useState} from 'react';
import CustomSnackbar from './CustomSnackBar';
import {SnackbarSeverity} from '../../../typedefs/error_types';

interface SnackbarGroupProps {
    show: boolean;
    message?: string;
    severity?: SnackbarSeverity;
}

const SnackbarComponent: React.FC<SnackbarGroupProps> = ({show, message = '', severity = SnackbarSeverity.ERROR}) => {
    const [snackbarOpen, setSnackbarOpen] = useState<boolean>(show);
    const [snackBarMessage, setSnackbarMessage] = useState<string>(message);
    const [snackBarSeverity, setSnackBarSeverity] = useState<SnackbarSeverity>(severity);

    return (
        <CustomSnackbar
            open={snackbarOpen}
            onClose={() => setSnackbarOpen(false)}
            severity={snackBarSeverity}
            message={snackBarMessage}
        />
    );
}

export default SnackbarComponent;