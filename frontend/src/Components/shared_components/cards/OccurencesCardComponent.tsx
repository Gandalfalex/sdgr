import {ModelOccurrence} from "../../../typedefs/spring_types";
import React, {useEffect, useState} from "react";
import {
    Box,
    Button,
    Dialog,
    DialogContent,
    DialogTitle,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableRow,
    Tooltip,
    Typography
} from "@mui/material";
import {Link as RouterLink} from 'react-router-dom';
import DeleteIcon from '@mui/icons-material/Delete';
import {DeleteDialog} from "../../dialogs/DeleteDialog";
import {deleteDataSet} from "../../../api/SpringAPI";
import {useSnackbar} from "../snackbar/SnackbarContext";
import {SnackbarSeverity} from "../../../typedefs/error_types";
import {useTranslation} from "react-i18next";


interface ConfigCardComponents {
    id: number;
    fetchOccurrences: (id: number) => Promise<Array<ModelOccurrence>>;
}


export const OccurrencesCardComponent = (props: ConfigCardComponents) => {
    const {id, fetchOccurrences} = props;
    const [occurrences, setOccurrences] = useState<Array<ModelOccurrence>>([]);
    const [showDelete, setShowDelete] = useState<boolean>(false);
    const [selectedProject, setSelectedProject] = useState<ModelOccurrence | null>(null);
    const [itemToDelete, setItemToDelete] = useState<ModelOccurrence | null>(null);
    const {showMessage} = useSnackbar();
    const { t } = useTranslation(['dialogs', 'headers', 'components']);

    const groupedOccurrences = occurrences.reduce((acc, curr) => {
        (acc[curr.projectId] = acc[curr.projectId] || []).push(curr);
        return acc;
    }, {} as Record<number, ModelOccurrence[]>);


    const deleteModel = () => {
        if (itemToDelete) {
            deleteDataSet(itemToDelete.projectId, itemToDelete.trackId, itemToDelete.dataSetId)
                .then(() => {
                    showMessage(t('delete_success', {ns: ['dialogs']}), SnackbarSeverity.INFO)

                    if (occurrences.length === 1) {
                        setSelectedProject(null)
                        setOccurrences([])
                    }
                    setOccurrences(occurrences.filter(o => o !== itemToDelete))
                })
                .catch(err => showMessage("Element not deleted" + err, SnackbarSeverity.ERROR))
        }
        setShowDelete(false);
    };

    useEffect(() => {
        fetchOccurrences(id).then(res => {
            setOccurrences(res);
        })
    }, [fetchOccurrences, id]);

    return (
        <div>
            {occurrences.length !== 0 ? (
                <Box>
                    <div>
                        <Typography>
                            {t("model_usages", {ns: ['headers']})}
                        </Typography>
                    </div>
                    {Object.values(groupedOccurrences).map((projectOccurrences) => (
                        <div key={projectOccurrences[0].projectId}
                             onClick={() => setSelectedProject(projectOccurrences[0])}>
                            <Typography color='#005c4b' component="p">
                                {projectOccurrences[0].projectName}
                            </Typography>
                        </div>)
                    )}
                </Box>
            ) : null}

            {selectedProject && (
                <Dialog onClose={() => {
                    setSelectedProject(null);
                }} open={Boolean(selectedProject)}>
                    <DialogTitle>{selectedProject.projectName}</DialogTitle>
                    <DialogContent>
                        <TableContainer>
                            <Table>
                                <TableBody>
                                    {groupedOccurrences[selectedProject.projectId]
                                        ? groupedOccurrences[selectedProject.projectId].map((occurrence) => (
                                            <TableRow key={occurrence.dataSetId}>
                                                <TableCell style={{borderRight: '1px solid #ccc'}}>
                                                    dataset {occurrence.dataSetName}
                                                </TableCell>
                                                <TableCell style={{borderRight: '1px solid #ccc'}}>
                                                    <Tooltip title={t('move_to', {ns: ['components']})}>
                                                        <Button
                                                            component={RouterLink}
                                                            to={`/project/${occurrence.projectId}?expandID=${occurrence.trackId}`}
                                                            style={{width: '200px', height: '40px'}}
                                                        >
                                                            Go to {occurrence.trackName}
                                                        </Button>
                                                    </Tooltip>
                                                </TableCell>
                                                <TableCell>
                                                    <Tooltip
                                                        title={t('delete_directly', {ns: ['components']})}>
                                                        <DeleteIcon
                                                            onClick={() => {
                                                                setShowDelete(true);
                                                                setItemToDelete(occurrence);
                                                            }}
                                                        >
                                                            Delete
                                                        </DeleteIcon>
                                                    </Tooltip>
                                                </TableCell>
                                            </TableRow>
                                        ))
                                        : null}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    </DialogContent>
                </Dialog>
            )}
            <DeleteDialog
                message={t('confirm_from_model_delete_action', {ns: ['dialogs']})}
                open={showDelete}
                onClose={() => setShowDelete(false)}
                onDelete={deleteModel}
            />
        </div>
    );
}