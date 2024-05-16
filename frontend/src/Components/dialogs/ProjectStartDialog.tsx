import {Button, Dialog, DialogActions, DialogContent, DialogTitle, TextField} from "@mui/material";
import React, {useMemo, useState} from "react";
import {getConfigurationForKafka} from "../../api/SpringAPI";
import {KafkaConfig} from "../../typedefs/spring_types";
import {useTranslation} from "react-i18next";
import {DialogActionComponent} from "./DialogActionsComponent";

export interface ProjectStartSendingDialogProps {
    open: boolean;
    onClose: () => void;
    startSending: () => void;
    projectId: number;
}


export const ProjectStartDialog = (props: ProjectStartSendingDialogProps) => {
    const {open, onClose, projectId, startSending} = props;
    const [kafkaConfig, setKafkaConfig] = useState<KafkaConfig|null>(null)
    const { t } = useTranslation(['dialogs']);
    const handleCancel = () => {
        onClose();
    };

     useMemo(() => {
         getConfigurationForKafka(projectId).then(res => {setKafkaConfig(res)})
    }, []);

     // TODO fix config
    return (
        <Dialog
            maxWidth="xs"
            open={open}
            onClose={onClose}
        >
            <DialogTitle>{"Start the sending process"}</DialogTitle>
            <DialogContent dividers>
                {kafkaConfig?.bootstrapServerAddress}
            </DialogContent>
            <DialogActionComponent
                onCancel={handleCancel}
                onConfirm={startSending}
                cancelText={t('button_label.cancel', {ns: ['dialogs']})}
                confirmText={t('button_label.start', {ns: ['dialogs']})}
            />
        </Dialog>
    );
}