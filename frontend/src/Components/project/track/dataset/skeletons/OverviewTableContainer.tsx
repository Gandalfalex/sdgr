import React from "react";
import {Table, TableBody, TableCell, TableContainer, TableRow} from "@mui/material";

interface OverviewProps {
    data: { labelText: string; value: number | string | undefined }[];
}

const OverviewTableContainer: React.FC<OverviewProps> = ({data}) => {

    return (
        <TableContainer>
            <Table size="small">
                <TableBody>
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

export default OverviewTableContainer;