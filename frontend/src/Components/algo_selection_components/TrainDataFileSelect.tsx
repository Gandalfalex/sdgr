import React, {useEffect, useMemo, useState} from 'react';
import {Autocomplete, Box, Checkbox, TextField} from "@mui/material";
import {TrainingData, TrainingDataFiles} from "../../typedefs/django_types";
import {useTranslation} from "react-i18next";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";


export interface TrainingDataSelectProps {
    selectedItems: number[];
    setSelectedFiles: React.Dispatch<React.SetStateAction<number[]>>;
    trainingDataFiles: Array<TrainingDataFiles>;
}


export const TrainingDataFileSelect: React.FC<TrainingDataSelectProps> = ({
                                                                          selectedItems,
                                                                          setSelectedFiles,
                                                                          trainingDataFiles
                                                                      }) => {
    const [selectedOptions, setSelectedOptions] = useState<TrainingDataFiles[]>([]);
    const {t} = useTranslation(['components']);

    const handleChange = (event: React.SyntheticEvent, value: TrainingDataFiles[]) => {
        setSelectedFiles(value.map(v => v.id));
        setSelectedOptions(value)
    };

    // Use your icons here
    const icon = <Checkbox/>;
    const checkedIcon = <Checkbox checked/>;

    useEffect(() => {
        const newSelectedOptions = trainingDataFiles.filter(trainingData =>
            selectedItems.includes(trainingData.id)
        );
        setSelectedOptions(newSelectedOptions);
    }, [selectedItems, trainingDataFiles])



    return (
        <Autocomplete
            multiple
            id="checkboxes-tags-demo"
            options={trainingDataFiles}
            disableCloseOnSelect
            getOptionLabel={(option) => option.name}
            renderOption={(props, option, {selected}) => (
                <li {...props}>
                    <Checkbox
                        icon={icon}
                        checkedIcon={checkedIcon}
                        style={{marginRight: 8}}
                        checked={selected}
                    />
                    {option.name}
                </li>
            )}
            style={{width: 500}}
            renderInput={(params) => (
                <TextField {...params} label={t('find_training_data_label', {ns: ['components']})}/>
            )}
            onChange={handleChange}
            value={selectedOptions}
        />);
};