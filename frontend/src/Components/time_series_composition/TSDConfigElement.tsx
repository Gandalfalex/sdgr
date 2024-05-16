import React, {useEffect, useState} from "react";
import {TrainDataPreviewDT, TSDConfig} from "../../typedefs/django_types";
import {
    deleteTsdConfigurationById,
    getAllTrainingDataForConfigReduced,
    getTsdConfigurationById,
    postCopyConfig,
} from "../../api/DjangoAPI";
import {Card, CardHeader,} from "@mui/material";
import {TSDSolutionCards} from "./helper_components/TSDSolutionCardComponents";
import {TSDConfigDialog} from "../dialogs/TSDConfigDialog";
import {CopyDialog} from "../dialogs/CopyDialog";
import {OptionsMenu} from "../shared_components/OptionsMenu";
import {AvatarDropDown} from "../shared_components/AvatarDropDown";
import {DeleteDialog} from "../dialogs/DeleteDialog";
import {SnackbarSeverity} from "../../typedefs/error_types";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {useTranslation} from "react-i18next";

interface TSDConfigurationElementProps {
    config: TSDConfig,
    onRefresh: () => void;
}

export const TSDConfigElement = (props: TSDConfigurationElementProps) => {
    const {config, onRefresh} = props;
    const [local_solution, setSolution] = useState<TSDConfig>(props.config);
    const [trainData, setTrainDataReduced] = useState<Array<TrainDataPreviewDT>>([]);
    const [showEditTSDSolutionDialog, setShowEditTSDSolutionDialog] = useState(false);
    const [expanded, setExpanded] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [showCopyDialog, setShowCopyDialog] = useState(false);
    const {showMessage} = useSnackbar();
    const { t } = useTranslation(['dialogs']);

    const handleExpandClick = () => {
        setExpanded(!expanded);
        getAllTrainingDataForConfigReduced(config.tsd_model, config.id).then(res => {
            setTrainDataReduced(res)
        })
    };


    const onUpdateRefresh = () => {
        getTsdConfigurationById(config.tsd_model, config.id)
            .then(res => {
                setSolution(res)
                showMessage(t('update_success', {ns: ['dialogs']}), SnackbarSeverity.SUCCESS)
            })
        onRefresh();
    };

    const closeNewMlSolutionDialog = () => {
        setShowEditTSDSolutionDialog(false);
    }


    const handleDelete = () => {
        deleteTsdConfigurationById(config.tsd_model, config.id)
            .then(() => {
                onRefresh();  // Trigger the refresh callback
                showMessage(t('delete_success', {ns: ['dialogs']}), SnackbarSeverity.INFO)
            })
            .catch(error => {
                showMessage("deletion failed: " + error, SnackbarSeverity.ERROR)
            });
    }

    const handleCopy = () => {
        postCopyConfig(config.tsd_model, config.id)
            .then(() => {
                onRefresh();  // Trigger the refresh callback
                setShowCopyDialog(false)
                showMessage(t('copy_element', {ns: ['dialogs']}), SnackbarSeverity.SUCCESS)
            })
            .catch(error => {
                showMessage("copy failed: " + error, SnackbarSeverity.ERROR)
            });
    }


    useEffect(() => {
        getTsdConfigurationById(config.tsd_model, config.id).then(res => {
            setSolution(res)
        })
    }, [config, onRefresh]);
    return (
        <>
            <Card>
                <CardHeader
                    avatar={
                        <AvatarDropDown handleExpandClick={handleExpandClick} expanded={expanded}/>
                    }
                    action={
                        <OptionsMenu
                            value={config}
                            setShowEditDialog={setShowEditTSDSolutionDialog}
                            setShowDeleteDialog={setShowDeleteDialog}
                            setShowCopyDialog={setShowCopyDialog}
                        />
                    }
                />
                <Card>
                    <TSDSolutionCards
                        config={config}
                        expanded={expanded}
                        trainData={trainData}
                    />
                </Card>
            </Card>

            {config && showEditTSDSolutionDialog && (
                <TSDConfigDialog
                    onUpdateRefresh={onUpdateRefresh}
                    id="new-config"
                    isEdit={true}
                    keepMounted
                    open={showEditTSDSolutionDialog}
                    onClose={() => {
                        setShowEditTSDSolutionDialog(false);
                        closeNewMlSolutionDialog();
                    }}
                    value={{
                        id: config.id,
                        name: config.name,
                        description: config.description,
                        created_at: config.created_at,
                        tsd_model: config.tsd_model,
                        imputation_algorithm: config.imputation_algorithm,
                        min_length: config.min_length,
                        train_data: config.train_data,
                        processing: config.processing,
                    }}
                />
            )}

            <DeleteDialog
                message={t('confirm_delete_action', {ns:['dialogs']})}
                open={showDeleteDialog}
                onClose={() => setShowDeleteDialog(false)}
                onDelete={handleDelete}
            />

            <CopyDialog
                open={showCopyDialog}
                onClose={() => setShowCopyDialog(false)}
                onCopy={handleCopy}/>
        </>
    );
}
