import React, {useState} from "react";
import {Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField} from "@mui/material";
import {putNewProject} from "../../api/SpringAPI";
import {useNavigate} from "react-router-dom";
import {useTranslation} from "react-i18next";
import {DialogActionComponent} from "./DialogActionsComponent";

export interface NewProjectDialogProps {
    open: boolean,
    onClose: () => void
}

const NewProjectDialog = (props: NewProjectDialogProps) => {
    const navigate = useNavigate();
    const {open, onClose} = props;
    const [name, setName] = useState<String>("");
    const { t } = useTranslation(['dialogs', 'headers']);
    const handleCancel = () => {
        onClose();
    };

    const handleCreate = () => {
        if (name.length > 0) {
            putNewProject(name).then((res: any) => {
                navigate(`/project/${res.id}`);
            }).catch((error) => {
                console.error("An error occurred while creating new project: ", error);
            });
        }
        onClose();
    };

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setName(event.target.value);
    };

    return (
        <Dialog
            maxWidth="xs"
            open={open}
            onClose={onClose}
        >
            <DialogTitle>{t('new_project', {ns: ['dialogs']})}</DialogTitle>
            <DialogContent dividers>
                <TextField required value={name} onChange={handleNameChange} variant="filled" label="Project name"/>
            </DialogContent>
            <DialogActionComponent
                onCancel={handleCancel}
                onConfirm={handleCreate}
                cancelText={t('button_label.cancel', {ns: ['dialogs']})}
                confirmText={t('button_label.create', {ns: ['dialogs']})}
                confirmDisabled={!name}
            />
        </Dialog>
    );
}

export default NewProjectDialog;