import React from 'react';
import {Box, Button, DialogActions} from "@mui/material";


interface IDialogActionProps {
    onCancel: () => void;
    onConfirm: () => void;
    confirmDisabled?: boolean;
    cancelText: string;
    confirmText: string;
}

export const DialogActionComponent: React.FC<IDialogActionProps> = ({ onCancel, onConfirm, cancelText, confirmText, confirmDisabled }) => {
    return (
        <DialogActions>
            <Button onClick={onCancel} color="primary">
                {cancelText}
            </Button>
            <Box flexGrow={1} />
            <Button onClick={onConfirm} color="primary" disabled={confirmDisabled}>
                {confirmText}
            </Button>
        </DialogActions>
    );
};
