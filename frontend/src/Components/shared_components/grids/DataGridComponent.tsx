import {Grid} from "@mui/material";
import React from "react";


interface DataGridComponentProps {
    children: React.ReactNode;
}

export const DataGridComponent: React.FC<DataGridComponentProps> = ({children, ...otherProps}) => {

    return (
        <Grid container
              direction="row"
              justifyContent="center"
              alignItems="center"
              spacing={3}>
            {children}
        </Grid>
    );
}