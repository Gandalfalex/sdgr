import {
    Button,
    Checkbox,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControlLabel,
    IconButton,
    MenuItem,
    TextField,
    Tooltip
} from "@mui/material";
import {Stack} from "@mui/system";
import React, {useEffect, useState} from "react";
import {DataTypeSchema, Track} from "../../typedefs/spring_types";
import {getDataTypes} from "../../api/SpringAPI";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select, {SelectChangeEvent} from "@mui/material/Select";
import HelpIcon from '@mui/icons-material/Help';
import {useTranslation} from "react-i18next";

export interface EditTrackDialogProps {
    id: string,
    keepMounted: boolean,
    value: Track,
    open: boolean,
    isEdit: boolean,
    onClose: (value?: Track) => void
}

export function TrackDialog(props: EditTrackDialogProps) {
    const {onClose, value: valueProp, open, isEdit, ...other} = props;
    const [value, setValue] = useState(valueProp);
    const [dataTypes, setDataTypes] = useState<Array<DataTypeSchema>>([]);
    const [selectedDataTypes, setSelectedDataTypes] = useState<Array<number>>([-1]);
    const { t } = useTranslation(['dialogs', 'headers']);

    useEffect(() => {
        if (!open) {
            setValue(valueProp);
            getDataTypes().then(res => setDataTypes(res));
        }
    }, [valueProp, open]);

    const handleCancel = () => {
        setSelectedDataTypes([-1])
        onClose();
    };

    const handleCreate = () => {
        let data = selectedDataTypes.map(pos => dataTypes[pos]).filter(type => undefined !== type);
        value.allowedDataTypes = data.length === 0 ? dataTypes : data;
        setSelectedDataTypes([-1])
        onClose(value);
    };

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue((oldValue) => ({
            ...oldValue,
            name: event.target.value
        }));
    };

    const handleSelectDataTypeChange = (event: SelectChangeEvent<typeof selectedDataTypes>) => {
        const {target: {value}} = event;
        setSelectedDataTypes(value as number[]);
    };

    const handleUnitChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue((oldValue) => ({
            ...oldValue,
            unit: event.target.value
        }));
    };

    const handleRepeatingChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue((oldValue) => ({
            ...oldValue,
            repeating: event.target.checked
        }));
    }

    return (
        <Dialog
            maxWidth="xs"
            open={open}
            {...other}
        >
            <DialogTitle>
                <div>
                    {isEdit ? t('update_track', {ns: ['dialogs']}) : t('new_track', {ns: ['dialogs']})}
                    <Tooltip
                        title={t('dialog_track_tooltip', {ns: ['dialogs']})}>
                        <IconButton size="small">
                            <HelpIcon fontSize="small"/>
                        </IconButton>
                    </Tooltip>
                </div>
            </DialogTitle>
            <DialogContent dividers>
                <Stack spacing={2}>
                    <div style={{display: 'flex', alignItems: 'center'}}>
                        <TextField
                            required
                            value={value.name}
                            onChange={handleNameChange}
                            size="small"
                            variant="filled"
                            label="Track name"
                            sx={{width: "10vw", minWidth: "200px", maxWidth: "400px"}}
                        />
                    </div>
                    <div style={{display: 'flex', alignItems: 'center'}}>
                        <TextField
                            required
                            value={value.unit}
                            onChange={handleUnitChange}
                            size="small"
                            variant="filled"
                            label="Unit"
                            sx={{width: "10vw", minWidth: "200px", maxWidth: "400px"}}
                        />
                    </div>
                    <FormControlLabel
                        control={<Checkbox checked={value.repeating} onChange={handleRepeatingChange}/>}
                        label="Repeating"
                    />
                    <div style={{display: 'flex', alignItems: 'center'}}>
                        <FormControl variant="filled" size="medium">
                            <InputLabel id="data-type-select-label" variant="filled">{t('data_types', {ns: ['headers']})}</InputLabel>
                            <Select
                                sx={{width: "10vw", minWidth: "200px", maxWidth: "400px"}}
                                labelId="data-type-select-label"
                                id="data-type-select"
                                multiple
                                value={selectedDataTypes}
                                onChange={handleSelectDataTypeChange}
                                variant="filled"
                            >
                                {dataTypes.map((dataType, index) => (
                                    <MenuItem key={index} value={index}>
                                        <Tooltip title={dataType.description}>
                                            <span>{dataType.name}</span>
                                        </Tooltip>
                                    </MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                    </div>
                </Stack>
            </DialogContent>
            <DialogActions>
                <Button autoFocus onClick={handleCancel}>{t('button_label.cancel', {ns: ['dialogs']})}</Button>
                <Button onClick={handleCreate}
                        disabled={!value.name || !value.unit}>{isEdit ? t('button_label.update', {ns: ['dialogs']}) : t('button_label.create', {ns: ['dialogs']})}</Button>
            </DialogActions>
        </Dialog>
    );
}
