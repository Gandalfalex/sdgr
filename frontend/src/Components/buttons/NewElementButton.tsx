import {IconButton, Tooltip, useTheme} from "@mui/material";
import AddIcon from "@mui/icons-material/Add";
import React from "react";

interface NewElementButtonProps {
    message: string;
    handleClick: (value: boolean) => void;
}

export const NewElementButton = (props: NewElementButtonProps) => {
    const {message, handleClick} = props;
    const theme = useTheme();

    return (<Tooltip title={message} arrow>
        <IconButton className={'growButton'} onClick={() => handleClick(true)}
                    sx={{
                        color: theme.palette.primary.main,
                        alignSelf: 'center'
                    }}>
            <AddIcon sx={{
                fontSize: 'xx-large'
            }}/>
        </IconButton>
    </Tooltip>)
}