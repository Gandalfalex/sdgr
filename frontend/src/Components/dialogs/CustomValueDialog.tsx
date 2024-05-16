import {Box, Dialog, DialogContent, DialogTitle, TextField, Typography} from "@mui/material";
import React, {useEffect, useState} from "react";
import {CustomValue, DataSet} from "../../typedefs/spring_types";
import {useTranslation} from "react-i18next";
import {DialogActionComponent} from "./DialogActionsComponent";

export interface AddDialogProps {
    dataSet: DataSet,
    onCreate: (value: CustomValue) => void,
    open: boolean,
    onClose: () => void
}

function CustomValueDialog(props: AddDialogProps) {
    const {onClose, onCreate, open, dataSet} = props;
    const [sampleNum, setSampleNum] = useState<String>("0");
    const [value, setValue] = useState<String>("0");
    const {t} = useTranslation(['dialogs', 'headers', 'components']);

    useEffect(() => {
        setValue("0");
        setSampleNum("0");

    }, [open]);

    const handleCreate = () => {
        if (isNaN(Number(value)) || isNaN(Number(sampleNum)) || !Number.isInteger(Number(sampleNum)) || value === "" || sampleNum === "")
            return;
        onCreate({value: Number(value), sampleNum: Number(sampleNum)});
        onClose();
    };

    const handlePositionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.value === "") {
            setSampleNum(event.target.value);
            return;
        }
        const newValue = Number(event.target.value)
        if (isNaN(newValue) || !Number.isInteger(newValue)) {
            return;
        }
        if (newValue > 0 && newValue < dataSet.numSamples) {
            setSampleNum(event.target.value);
        }

    };

    const handleValueChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.value === "") {
            setValue(event.target.value);
            return;
        }
        const newValue = Number(event.target.value)
        if (isNaN(newValue)) return;
        setValue(event.target.value);
    };

    return (
        <Dialog
            maxWidth="xs"
            open={open}
        >
            <DialogTitle>{t('custom_value_dialog', {ns: ['headers']})}</DialogTitle>
            <DialogContent dividers>
                <TextField required value={sampleNum} onChange={handlePositionChange} variant="filled"
                           label="Position in dataset"/>
                <Box overflow={"hidden"} sx={{width: 218}}>
                    <Typography color={"gray"} variant="caption" display="inline-block" onChange={handlePositionChange}>Sending
                        time relative to dataset:
                    </Typography>
                    <Typography color={"gray"} variant="caption" display="inline-block"
                                sx={{mt: 0}}>{(!isNaN(Number(sampleNum))) ? Number(sampleNum) / dataSet.frequency : "---"} sec</Typography>
                </Box>
                <TextField
                    required
                    type="number"
                    value={value}
                    onChange={handleValueChange}
                    variant="filled"
                    label={t('single_value_value', {ns: ['components']})}/>
            </DialogContent>
            <DialogActionComponent
                onCancel={onClose}
                onConfirm={handleCreate}
                cancelText={t('button_label.cancel', {ns: ['dialogs']})}
                confirmText={t('button_label.create', {ns: ['dialogs']})}
                confirmDisabled={(value === "" || sampleNum === "")}
            />
        </Dialog>
    );
}

export default CustomValueDialog;