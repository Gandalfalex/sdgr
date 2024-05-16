import {Card, CardContent, CardHeader, Grid, PaperProps, useTheme} from "@mui/material";
import React from "react";

interface ElementCardComponentProps extends PaperProps {
    children: React.ReactNode;
    header?: string;
}

export const ElementCardComponent: React.FC<ElementCardComponentProps> = ({children, header, ...otherProps}) => {
    const theme = useTheme();
    return (
        <div>
            <Card style={{boxShadow: "none", backgroundColor: theme.palette.secondary.light}}>
                <CardHeader sx={{pl: 5, pt: 4}} title={header}/>
            </Card>
            <CardContent>
                <Grid
                    container
                    gap={2}
                    wrap="nowrap"
                    direction="column"
                    justifyContent="flex-start"
                    alignItems="stretch"
                    sx={{
                        minHeight: '80vh',
                        maxHeight: "90vh",
                        width: "100%",
                        p: 1,
                        pt: 0,
                        overflowY: 'auto'
                    }}
                >
                    {children}
                </Grid>
            </CardContent>
        </div>
    );
};