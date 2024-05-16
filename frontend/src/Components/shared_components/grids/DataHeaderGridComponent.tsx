import React from "react";
import {Grid, Typography, useTheme} from "@mui/material";

interface DataHeaderGridComponentProps {
    children?: React.ReactNode;
    header: string;
}

export const DataHeaderGridComponent: React.FC<DataHeaderGridComponentProps> = ({children, header, ...otherProps}) => {

    const theme = useTheme();

    return <Grid container item xs="auto"
                 spacing={1}
                 direction={"column"}
                 justifyContent="center"
                 alignItems="center">
        <Grid item xs={3}>
            <Typography color={theme.palette.background.paper} variant={"h4"} m={4}>
                {header}
            </Typography>
        </Grid>
        {children}
    </Grid>
}