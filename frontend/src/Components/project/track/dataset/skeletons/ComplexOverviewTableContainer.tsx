import React from "react";
import {Table, TableBody, TableCell, TableContainer, TableRow} from "@mui/material";

interface ModelOverViewProps {
    model: string | undefined;
    configuration: string | undefined;
    trainingDataSize: number;
    data: { labelText: string; value: number | string | undefined }[];
}

const ComplexOverviewTableContainer: React.FC<ModelOverViewProps> = ({
                                                                         data,
                                                                         model,
                                                                         configuration,
                                                                         trainingDataSize
                                                                     }) => {

    return (
        <TableContainer>
            <Table size="small">
                <TableBody>
                    <TableRow key={model}>
                        <TableCell>
                            Model
                        </TableCell>
                        <TableCell>
                            {model}
                        </TableCell>
                    </TableRow>

                    <TableRow key={configuration}>
                        <TableCell>
                            configuration
                        </TableCell>
                        <TableCell>
                            {configuration}
                        </TableCell>
                    </TableRow>

                    <TableRow key={trainingDataSize}>
                        <TableCell>
                            trainingDataSize
                        </TableCell>
                        <TableCell>
                            {trainingDataSize}
                        </TableCell>
                    </TableRow>
                    {data.map(row => {
                        return (
                            <TableRow key={row.labelText}>
                                <TableCell>
                                    {row.labelText}
                                </TableCell>
                                <TableCell>
                                    {row.value}
                                </TableCell>
                            </TableRow>
                        )
                    })}
                </TableBody>
            </Table>
        </TableContainer>
    )
}

export default ComplexOverviewTableContainer;