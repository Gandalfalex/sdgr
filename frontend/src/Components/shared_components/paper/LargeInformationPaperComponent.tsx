import {Paper, PaperProps, Typography} from "@mui/material";
import {Stack} from "@mui/system";
import React from "react";


interface InformationPaperComponentProps extends PaperProps {
    children: React.ReactNode;
    header?: string;

}


export const LargeInformationPaperComponent: React.FC<InformationPaperComponentProps> = ({
                                                                                             children,
                                                                                             header,
                                                                                             ...otherProps
                                                                                         }) => {
    return (
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh'}}>
            <Paper key={"header_key"} elevation={2} style={{width: '30vw', padding: '16px', height: '80vh', overflow: 'auto'}}>
                <Stack spacing={{xs: 1, sm: 2, md: 4}}>
                    {header
                        ? <Typography variant="h6">
                            {header}
                        </Typography>
                        : null}
                    {children}
                </Stack>
            </Paper>
        </div>
    );
};