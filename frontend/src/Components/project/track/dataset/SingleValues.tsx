import {
    Box,
    IconButton,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Tooltip
} from "@mui/material";
import {useEffect, useState} from "react";
import {CustomValue, DataSet} from "../../../../typedefs/spring_types";
import ClearIcon from "@mui/icons-material/Clear";
import AddIcon from "@mui/icons-material/Add";
import CustomValueDialog from "../../../dialogs/CustomValueDialog";
import {useTranslation} from "react-i18next";

interface Props {
    dataSet: DataSet,
    updateDataSet: (newDataSet: DataSet) => void
}

export const SingleValues = (props: Props) => {
    const [showDialog, setDialog] = useState(false);
    const {dataSet, updateDataSet} = props;
    const {t} = useTranslation(['components']);

    const createNewCustomValue = (newValue: CustomValue) => {
        if (dataSet.numSamples <= newValue.sampleNum) return;
        let data = {...dataSet};
        data.customValues.push(newValue);
        updateDataSet(data);
    }
    const deleteCustomValue = (newValue: CustomValue) => {
        if (dataSet) {
            let data = dataSet;
            const index = data.customValues.indexOf(newValue);
            if (index > -1) {
                data.customValues.splice(index, 1);
            }
            updateDataSet(data);
        }
    }


    const handleOpen = () => {
        setDialog(true);
    };
    const handleClose = () => {
        setDialog(false);
    };

    useEffect(() => {
    }, [dataSet])
    return (<Box sx={{overflow: "auto"}}>
        <TableContainer sx={{maxHeight: "240px"}}>
            <Table size="small" stickyHeader>
                <TableHead>
                    <TableRow>
                        <TableCell>
                            {t('single_value_position', {ns: ['components']})}
                        </TableCell>
                        <TableCell>
                            {t('single_value_value', {ns: ['components']})}
                        </TableCell>
                        <TableCell width="10%">
                            <Tooltip title="Create new entry" arrow>
                                <IconButton size={"small"} onClick={handleOpen} style={{padding: 0}}>
                                    <AddIcon fontSize="small"/>
                                </IconButton>
                            </Tooltip>
                        </TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {dataSet ? dataSet.customValues.map((pair, index) =>
                        <TableRow key={index}>
                            <TableCell>
                                {pair.sampleNum}
                            </TableCell>
                            <TableCell>
                                {pair.value}
                            </TableCell>
                            <TableCell>
                                <Tooltip title={t('single_value_delete_entry', {ns: ['components']})} arrow>
                                    <IconButton size={"small"} onClick={() => {
                                        deleteCustomValue(pair)
                                    }} style={{padding: 0}}>
                                        <ClearIcon fontSize="small"/>
                                    </IconButton>
                                </Tooltip>
                            </TableCell>
                        </TableRow>
                    ) : <TableRow/>}
                </TableBody>
            </Table>
        </TableContainer>
        <CustomValueDialog
            dataSet={dataSet}
            open={showDialog}
            onCreate={createNewCustomValue}
            onClose={handleClose}/>
    </Box>);
}