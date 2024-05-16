import ArrowDropDownIcon from "@mui/icons-material/ArrowDropDown";
import React, {forwardRef} from "react";

import {Avatar, Tooltip, useTheme} from "@mui/material";
import {useTranslation} from "react-i18next";


interface AvatarDropDownProps {
    handleExpandClick: () => void;
    expanded: boolean;
}

export const AvatarDropDown = forwardRef<HTMLDivElement, AvatarDropDownProps>(({handleExpandClick, expanded}, ref) => {
    const theme = useTheme();
    const { t } = useTranslation(['components']);
    return (
        <Tooltip title={t('graphic_train_data_display', {ns: ['components']})}>
            <Avatar
                ref={ref}
                className={'growButton'}
                sx={{bgcolor: theme.palette.background.paper}}
                onClick={function expand() {
                    handleExpandClick();
                }}
            >
                <ArrowDropDownIcon
                    sx={{
                        color: theme.palette.text.secondary,
                        bgcolor: theme.palette.background.paper,
                        transform: expanded ? 'rotate(0deg)' : 'rotate(-90deg)',
                        transition: 'transform 0.3s',
                        fontSize: '2rem'
                    }}
                />
            </Avatar>
        </Tooltip>
    );
});
