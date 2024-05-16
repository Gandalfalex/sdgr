import {Paper, PaperProps, Typography} from "@mui/material";
import {Stack} from "@mui/system";
import React from "react";


interface InformationPaperComponentProps extends PaperProps {
    children: React.ReactNode;
    header?: string;

}


export const InformationPaperComponent: React.FC<InformationPaperComponentProps> = ({children, header, ...otherProps}) => {
    return (
        <Paper key={"header_key"} elevation={2} style={{ width: '20vw', padding: '16px', height: 'auto' }}>
            <Stack spacing={{ xs: 1, sm: 2, md: 4 }}>
                {header
                    ? <Typography variant="h6">
                    {header}
                </Typography>
                : null }
                {children}
            </Stack>
        </Paper>
    );
};