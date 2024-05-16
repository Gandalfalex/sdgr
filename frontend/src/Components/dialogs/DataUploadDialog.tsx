import {Dialog, DialogContent, DialogTitle, IconButton, Tooltip, Typography} from "@mui/material";
import {FileDropzone} from "../algo_selection_components/FileDropZone";
import React, {useState} from "react";
import {ListItemSection} from "../algo_selection_components/ListItemSelection";
import HelpIcon from "@mui/icons-material/Help";
import {uploadTrainingFiles} from "../../api/DjangoAPI";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../../typedefs/error_types";
import {useTranslation} from "react-i18next";
import {DialogActionComponent} from "./DialogActionsComponent";

interface DialogProps {
    open: boolean,
    onClose: () => void
}

export const DataUploadDialog = (props: DialogProps) => {
    const {open, onClose} = props;
    const [selectedUploadFiles, setSelectedUploadFiles] = useState<Array<File>>([])
    const {showMessage} = useSnackbar();
    const {t} = useTranslation(['dialogs', 'headers']);

    const onDrop = React.useCallback((acceptedFiles: File[]) => {
        setSelectedUploadFiles(acceptedFiles);
    }, []);

    const startUpload = () => {
        uploadTrainingFiles(selectedUploadFiles)
            .then(
                res => {
                    showMessage("Data uploaded", SnackbarSeverity.SUCCESS)
                }
            )
        onClose();
    }

    return <Dialog open={open} maxWidth="lg">
        <DialogTitle>
            <div>
                <Typography variant="h5">
                    {"Upload new Data"}
                    <Tooltip
                        title={t('dialog_upload_tooltip', {ns: ['dialogs']})}>
                        <IconButton size="small">
                            <HelpIcon fontSize="small"/>
                        </IconButton>
                    </Tooltip>
                </Typography>
                <Typography variant="h6">
                    {t('dialog_upload_drag_n_drop_message', {ns: ['dialogs']})}
                </Typography>
            </div>
        </DialogTitle>
        <DialogContent>
            <FileDropzone onDrop={onDrop}/>
            <ListItemSection
                selectedFiles={selectedUploadFiles}
                trainingDataSets={[]}
                setSelectedFiles={setSelectedUploadFiles}
                selectedTrainingDataFiles={[]}
                trainingDataSetFiles={[]}/>
        </DialogContent>
        <DialogActionComponent
            onCancel={onClose}
            onConfirm={startUpload}
            cancelText={t('button_label.cancel', {ns: ['dialogs']})}
            confirmText={t('button_label.upload', {ns: ['dialogs']})}
        />
    </Dialog>
}