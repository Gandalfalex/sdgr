import React from "react";
import {Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle} from "@mui/material";
import {useTranslation} from "react-i18next";
import {DialogActionComponent} from "./DialogActionsComponent";

interface CopyDialogProps {
    open: boolean;
    onClose: () => void;
    onCopy: () => void;
}

export const CopyDialog: React.FC<CopyDialogProps> = ({open, onClose, onCopy}) => {
    const { t } = useTranslation(['dialogs', 'headers']);
    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{t('copy_dialog', {ns: ['headers']})}</DialogTitle>
            <DialogContent>
                <DialogContentText>
                    {t('dialog_copy_context', {ns: ['dialogs']})}
                </DialogContentText>
            </DialogContent>
            <DialogActionComponent
                onCancel={onClose}
                onConfirm={() => {
                    onCopy();
                    onClose();
                }}
                cancelText={t('button_label.cancel', {ns: ['dialogs']})}
                confirmText={t('button_label.confirm', {ns: ['dialogs']})}
            />
        </Dialog>
    );
};

