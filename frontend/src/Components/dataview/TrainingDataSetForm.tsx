import {Card, CardHeader} from "@mui/material";
import {OptionsMenu} from "../shared_components/OptionsMenu";
import React, {useState} from "react";
import {TrainingData} from "../../typedefs/django_types";
import {deleteSpecificTrainingData} from "../../api/DjangoAPI";
import {DataViewComponents} from "./DataViewComponents";
import {DeleteDialog} from "../dialogs/DeleteDialog";
import {SnackbarSeverity} from "../../typedefs/error_types";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {useTranslation} from "react-i18next";


interface TrainingDataSetProp {
    data: TrainingData;
    onRefresh: () => void;
}

export const TrainingDataSetForm = (props: TrainingDataSetProp) => {
    const {data, onRefresh} = props;
    const [showDelete, setShowDelete] = useState<boolean>(false);
    const {showMessage} = useSnackbar();
    const { t } = useTranslation(['dialogs', 'headers']);

    const handleDelete = () => {
        deleteSpecificTrainingData(data.id)
            .then(() => {
                showMessage("Element deleted", SnackbarSeverity.SUCCESS)
            })
            .catch(error => {
                showMessage("deletion failed: " + error, SnackbarSeverity.ERROR)
            });
        onRefresh();
    }

    return <Card>
        <CardHeader
            action={
                <OptionsMenu
                    value={data}
                    setShowDeleteDialog={setShowDelete}
                />
            }
        />
        <DataViewComponents data={data}/>
        <DeleteDialog
            message={t('data_set_list_delete_question', {ns: ['headers']})}
            open={showDelete}
            onClose={() => setShowDelete(false)}
            onDelete={handleDelete}
        />
    </Card>
}
