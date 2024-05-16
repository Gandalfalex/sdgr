import React, {useEffect, useMemo, useState} from 'react';
import {Autocomplete, Checkbox, TextField} from "@mui/material";
import {TrainingData} from "../../typedefs/django_types";
import {useTranslation} from "react-i18next";


export interface TrainingDataSelectProps {
    selectedItems: number[];
    setSelectedItems: React.Dispatch<React.SetStateAction<number[]>>;
    trainingDataSets: Array<TrainingData>;
}


export const TrainingDataItemSelect: React.FC<TrainingDataSelectProps> = ({
                                                                          selectedItems,
                                                                          setSelectedItems,
                                                                          trainingDataSets
                                                                      }) => {
    const [selectedOptions, setSelectedOptions] = useState<TrainingData[]>([]);
    const {t} = useTranslation(['components']);

    const handleChange = (event: React.SyntheticEvent, value: TrainingData[]) => {
        setSelectedItems(value.map(v => v.id));
        setSelectedOptions(value)
    };

    // Use your icons here
    const icon = <Checkbox/>;
    const checkedIcon = <Checkbox checked/>;

    useEffect(() => {
        const newSelectedOptions = trainingDataSets.filter(trainingData =>
            selectedItems.includes(trainingData.id)
        );
        setSelectedOptions(newSelectedOptions);
    }, [selectedItems, trainingDataSets]);

    return (<Autocomplete
        multiple
        id="checkboxes-tags-demo"
        options={trainingDataSets}
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