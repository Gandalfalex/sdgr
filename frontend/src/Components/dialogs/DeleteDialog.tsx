import React from "react";
import {Dialog, DialogContent, DialogContentText, DialogTitle} from "@mui/material";
import {useTranslation} from "react-i18next";
import {DialogActionComponent} from "./DialogActionsComponent";

interface DeleteDialogProps {
    message: string
    open: boolean;
    onClose: () => void;
    onDelete: () => void;
}

export const DeleteDialog: React.FC<DeleteDialogProps> = ({open, onClose, onDelete, message}) => {
    const {t} = useTranslation(['dialogs', 'headers']);
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{t('delete_dialog', {ns: ['headers']})}</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    {message}
                </DialogContentText>
            </DialogContent>
            <DialogActionComponent
                onCancel={onClose}
                onConfirm={() => {
                    onDelete();
                    onClose();
                }}
                cancelText={t('button_label.cancel', {ns: ['dialogs']})}
                confirmText={t('button_label.confirm', {ns: ['dialogs']})}
            />
        </Dialog>
    );
};

