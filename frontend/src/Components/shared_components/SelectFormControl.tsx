import React from 'react';
import FormControl from '@mui/material/FormControl';
import Select, {SelectChangeEvent} from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import InputLabel from "@mui/material/InputLabel";
import {OutlinedInput} from "@mui/material";

interface SelectItem {
    id: number;
    name: string;
}

interface SelectFormControlProps {
    label: string;
    value: number | undefined | number[];
    handleChange: (event: SelectChangeEvent<number | number[]>) => void;
    items: SelectItem[];
    id: string;
    multiple?: boolean;
}

export const SelectFormControl: React.FC<SelectFormControlProps> = ({label, value, handleChange, items, id, multiple}) => {

    const ITEM_HEIGHT = 48;
    const ITEM_PADDING_TOP = 8;
    const MenuProps = {
        PaperProps: {
            style: {
                maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
                width: 250,
            },
        },
    };


    const renderLabel = () => {
        if (multiple) {
            return label;
        } else {
            const selectedItem = items.find(item => item.id === value);
            return selectedItem ? selectedItem.name : label;
        }
    };


    return (
        <FormControl sx={{m: 1, width: 300}}>
            <InputLabel id={id + "Label"}>{renderLabel()}</InputLabel>
            <Select
                multiple={multiple}
                value={value === undefined ? '' : value}
                onChange={handleChange}
                input={<OutlinedInput label={label}/>}
                labelId={id + "Label"}
                id={id}
                sx={{minWidth: 100}}
                MenuProps={MenuProps}
            >
                {items.map((item) => (
                    <MenuItem key={item.id} value={item.id}>
                        {item.name}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}
