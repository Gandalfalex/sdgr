import React, {useEffect, useState} from "react";
import {MlConfig, TrainDataPreviewDT} from "../../typedefs/django_types";
import {
    copySolutionSet,
    deleteSolutionByID,
    getAllTrainingDataForSolutionReduced,
    getMlConfigByModelIdAndConfigId,
} from "../../api/DjangoAPI";
import {Card, CardHeader} from "@mui/material";
import {CopyDialog} from "../dialogs/CopyDialog";
import {OptionsMenu} from "../shared_components/OptionsMenu";
import {AvatarDropDown} from "../shared_components/AvatarDropDown";
import {DeleteDialog} from "../dialogs/DeleteDialog";
import {SnackbarSeverity} from "../../typedefs/error_types";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {MLConfigCardComponents} from "./helper_components/MLConfigCardComponent";
import {MlConfigDialog} from "../dialogs/MlConfigDialog";

interface MlConfigElementProps {
    config: MlConfig,
    onRefresh: (configId: number) => void;
}

export const MlConfigElement = (props: MlConfigElementProps) => {
    const {config, onRefresh} = props;
    const [local_configs, setConfigs] = useState<MlConfig>(props.config);
    const [trainData, setTrainDataReduced] = useState<Array<TrainDataPreviewDT>>([]);
    const [showEditMLConfigDialog, setShowEditMLConfigDialog] = useState(false);
    const [showCopyDialog, setShowCopyDialog] = useState(false);
    const [expanded, setExpanded] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const {showMessage} = useSnackbar();

    const handleExpandClick = () => {
        setExpanded(!expanded);
        getAllTrainingDataForSolutionReduced(config.ml_model, config.id).then(res => {
            setTrainDataReduced(res)
        })
    };


    const onUpdateRefresh = () => {
        getMlConfigByModelIdAndConfigId(config.ml_model, config.id)
            .then(res => {
                setConfigs(res)
                showMessage("Updated element", SnackbarSeverity.SUCCESS)
            })
        onRefresh(config.id);
    };

    const closeNewMlSolutionDialog = () => {
        setShowEditMLConfigDialog(false);
    }

    const handleDelete = () => {
        deleteSolutionByID(config.ml_model, config.id)
            .then(() => {
                onRefresh(config.id);
                showMessage("Element deleted", SnackbarSeverity.SUCCESS)
            })
            .catch(error => {
                showMessage("deletion failed: " + error, SnackbarSeverity.ERROR)
            });
    }

    const handleCopy = () => {
        copySolutionSet(config.ml_model, config.id)
            .then(() => {
                onRefresh(config.id);  // Trigger the refresh callback
                setShowCopyDialog(false)
                showMessage("Element copied", SnackbarSeverity.SUCCESS)
            })
            .catch(error => {
                showMessage("copy failed: " + error, SnackbarSeverity.ERROR)
            });
    }


    useEffect(() => {
        getMlConfigByModelIdAndConfigId(config.ml_model, config.id).then(res => {
            setConfigs(res)
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
                            setShowEditDialog={setShowEditMLConfigDialog}
                            setShowDeleteDialog={setShowDeleteDialog}
                            setShowCopyDialog={setShowCopyDialog}
                        />
                    }
                />
                <MLConfigCardComponents
                    config={config}
                    expanded={expanded}
                    trainData={trainData}
                    onUpdate={() => onRefresh}
                />
            </Card>

            {config && showEditMLConfigDialog
                ? (
                    <MlConfigDialog
                        onUpdateRefresh={onUpdateRefresh}
                        id="new-track"
                        isEdit={true}
                        keepMounted
                        open={showEditMLConfigDialog}
                        onClose={() => {
                            setShowEditMLConfigDialog(false);
                            closeNewMlSolutionDialog();
                        }}
                        value={{
                            id: config.id,
                            name: config.name,
                            description: config.description,
                            created_at: config.created_at,
                            solution_id: config.solution_id,
                            is_running: config.is_running,
                            imputation_algorithm: config.imputation_algorithm,
                            min_length: config.min_length,
                            ml_model: config.ml_model,
                            train_data: config.train_data,
                            processing: config.processing
                        }}
                    />
                ) : null}

            <DeleteDialog
                message={"Are you sure you want to delete this ml configuration?"}
                open={showDeleteDialog}
                onClose={() => setShowDeleteDialog(false)}
                onDelete={handleDelete}
            />

            <CopyDialog
                open={showCopyDialog}
                onClose={() => setShowCopyDialog(false)}
                onCopy={handleCopy}
            />
        </>
    );
}