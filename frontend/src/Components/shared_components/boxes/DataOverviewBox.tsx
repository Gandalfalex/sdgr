import {Box, useTheme} from "@mui/material";
import React from "react";

interface DataGridBoxProps {
    children: React.ReactNode;
}

export const DataOverviewBox: React.FC<DataGridBoxProps> = ({children, ...otherProps}) => {
    const theme = useTheme();

    return <Box
        className={'grow'}
        bgcolor={theme.palette.background.paper}
        sx={{
            width: '100%',
            maxHeight: '100%',
            borderRadius: '16px',
            boxShadow: "0px 0px 10px 5px rgb(0,0,0,0.2)",
        }}>
        <Box
            bgcolor={theme.palette.background.paper}
            sx={{
                mr: 2,
                ml: 2,
                maxHeight: '60vh',
                overflow: 'auto'
            }}
        >
            {children}
        </Box>
    </Box>
}