import React, {useMemo, useState} from "react";
import {TrainingData} from "../../typedefs/django_types";
import {TrainingDataSetForm} from "./TrainingDataSetForm";
import {deleteTrainingDataForFiles, getTrainingDataForFiles} from "../../api/DjangoAPI";
import {Card, CardHeader, List, ListItem} from "@mui/material";
import {DeleteDialog} from "../dialogs/DeleteDialog";
import {OptionsMenu} from "../shared_components/OptionsMenu";
import {useTranslation} from "react-i18next";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../../typedefs/error_types";

interface FileProps {
    fileId: number;
    onRefresh: () => void;
}

export const ListDataSetComponents = (props: FileProps) => {
    const {fileId, onRefresh} = props;
    const [trainingDataSets, setTrainingDataSets] = useState<Array<TrainingData>>([])
    const [showDelete, setShowDelete] = useState<boolean>(false)
    const {t} = useTranslation(['dialogs', 'headers', 'errors']);
    const {showMessage} = useSnackbar();

    const refresh = () => {
        getTrainingDataForFiles(fileId).then(res => {
            setTrainingDataSets(res)
        })
    }

    const handleDelete = () => {
        deleteTrainingDataForFiles(fileId)
            .then(res => {
                if (res !== null) {
                    console.log("sdfg")
                }
            })
            .catch(error => {
                console.log(error.response.data)
                showMessage(t(error.response.data.i18nKey, {ns: ['errors']}), SnackbarSeverity.ERROR)
            });
    }

    useMemo(() => {
        getTrainingDataForFiles(fileId).then(res => {
            setTrainingDataSets(res)
        })
    }, []);

    return (
        <Card>
            <CardHeader action={
                <OptionsMenu
                    value={fileId}
                    setShowDeleteDialog={setShowDelete}
                />
            }>
            </CardHeader>
            <List sx={{display: 'flex', flexDirection: 'row', overflowX: 'auto'}}>
                {trainingDataSets.length !== 0 ?
                    trainingDataSets.map((config) => (
                        <ListItem key={config.id}>
                            <TrainingDataSetForm data={config} onRefresh={refresh}/>
                        </ListItem>
                    ))
                    : null
                }
            </List>
            <DeleteDialog
                message={t('data_set_list_delete_question', {ns: ['headers']})}
                open={showDelete}
                onClose={() => setShowDelete(false)}
                onDelete={handleDelete}
            />
        </Card>)

}