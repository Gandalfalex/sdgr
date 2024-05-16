import React, {useEffect, useState} from "react";
import {TrainDataPreviewComplete, TSDConfig} from "../../typedefs/django_types";
import {postPreprocessorConfigTSD, uploadForPreview} from "../../api/DjangoAPI";
import {InformationTextField} from "../algo_selection_components/InformationTextField";
import {PreprocessorSchema} from "../algo_selection_components/PreprocessorSchema";
import {useHandleTSDConfigAPI} from "../../api/django_hooks/TSAConfigHook";
import {StepperDialog} from "./StepperDialog";
import {useTranslation} from "react-i18next";
import {DataSelectionComponent} from "../algo_selection_components/DataSelectionComponent";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";


export interface EditTSCConfigDialog {
    id: string,
    keepMounted: boolean,
    value: TSDConfig,
    open: boolean,
    isEdit: boolean,
    onClose: (value?: TSDConfig) => void
    onUpdateRefresh: () => void;
}

const set_initial_data = (value: TSDConfig) => {
    return {
        min_length: value.min_length,
        Imputation_Algorithm: value.imputation_algorithm?.name,
        "Processor Type": value.processing?.typeName
    }
}

export function TSDConfigDialog(props: EditTSCConfigDialog) {
    const {onClose, value: valueProp, open, isEdit, onUpdateRefresh} = props;
    const [value, setValue] = useState(valueProp);

    const [selectedFiles, setSelectedFiles] = React.useState<File[]>([]);
    const [selectedItems, setSelectedItems] = React.useState<number[]>([]);
    const {t} = useTranslation(['dialogs', 'headers']);
    const [openBackDrop, setOpenBackDrop] = React.useState(false);
    const {handleTSDConfigAPI, loading, error} = useHandleTSDConfigAPI();
    const steps = [t('multi_dialog_step_info', {ns: ['dialogs']}), t('multi_dialog_step_data', {ns: ['dialogs']}), t('multi_dialog_step_preview', {ns: ['dialogs']})];
    const [selectedTrainingFiles, setSelectedTrainingFiles] = React.useState<number[]>([]);

    const [trainDataPreview, setTrainDataPreview] = useState<TrainDataPreviewComplete | undefined>(undefined);

    const [isPreprocessorValid, setIsPreprocessorValid] = useState(false);
    const [activeStep, setActiveStep] = useState(0)
    const [dataSetFormState, setDataSetFormState] = useState<any>({
        formData: props.value.min_length ? set_initial_data(props.value) : {}
    });

    const resetValues = () => {
        setValue(valueProp);
        setDataSetFormState({formData: {}})
        setSelectedFiles([]);
        setSelectedItems([]);
        setActiveStep(0)
    };

    const handleCancel = () => {
        onClose();
        resetValues();
    };

    const handleSuccess = (data: any) => {
        console.log(data)
    };

    const handleCreate = async () => {
        setOpenBackDrop(true);
        try {
            await handleTSDConfigAPI(isEdit, value, selectedItems, selectedFiles, selectedTrainingFiles, handleSuccess)
                .then(res => {
                    setValue(res)
                    postPreprocessorConfigTSD(res.tsd_model, res.id, dataSetFormState.formData).then(res => console.log(res));
                })
        } catch (error) {
            console.error("Error during the operation:", error);
        } finally {
            setOpenBackDrop(false);
        }
        onClose(value);
        onUpdateRefresh();
        resetValues();
    };

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue((oldValue) => ({
            ...oldValue,
            name: event.target.value
        }));
    };

    const handleEnableSubmit = (isEnabled: boolean) => {
        setIsPreprocessorValid(isEnabled);
    };


    const handleDescriptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setValue((oldValue) => ({
            ...oldValue,
            description: event.target.value
        }));
    };

    const handlePreviewSubmit = async () => {
        const id = selectedItems.length !== 0 ? selectedItems[0] : undefined;
        const fileID = selectedTrainingFiles.length !== 0 ? selectedTrainingFiles[0] : undefined;
        return uploadForPreview(selectedFiles, dataSetFormState.formData, id, fileID)
            .then(res => {
                setTrainDataPreview(res);
            });
    };

    const getStepContent = (step: number) => {
        switch (step) {
            case 0: // set name and description
                return (
                    <InformationTextField
                        onChangeDescription={handleDescriptionChange}
                        onChangeName={handleNameChange}
                        valueDescription={value.description}
                        valueName={value.name}/>);
            case 1: // upload or select data
                return <DataSelectionComponent
                    selectedItems={selectedItems}
                    setSelectedItems={setSelectedItems}
                    selectedFiles={selectedFiles}
                    setSelectedFiles={setSelectedFiles}
                    selectedTrainFiles={selectedTrainingFiles}
                    setSelectedTrainFiles={setSelectedTrainingFiles}
                />;
            case 2:
                return (
                    value !== undefined
                        ? <PreprocessorSchema
                            postPreview={handlePreviewSubmit}
                            data={trainDataPreview}
                            isPreprocessorValid={handleEnableSubmit}
                            dataSetFormState={dataSetFormState}
                            setDataSetFormState={setDataSetFormState}
                        />
                        : <div/>
                );
            default:
                return <div/>
        }
    };

    const isSubmittable = () => {
        let message = "";
        let sendable = true;
        if (value.name === "") {
            message = "Name is required \n"
            sendable = false;
        }
        if (selectedFiles.length === 0 && selectedItems.length === 0 && selectedTrainingFiles.length === 0) {
            message = message + "Please select some data"
            sendable = false;
        }
        return {
            validInput: sendable,
            validConfiguration: isPreprocessorValid,
            message: message
        };
    }

    useEffect(() => {
        if (isEdit) {
            setSelectedItems(value.train_data)
        }
        if (!open) {
            setValue(valueProp);
        }
    }, [valueProp, open, isEdit, value]);
    return (
        <StepperDialog
            open={open}
            steps={steps}
            getStepContent={getStepContent}
            handleCancel={handleCancel}
            send={handleCreate}
            isEdit={isEdit}
            isSubmittable={isSubmittable}
            activeStep={activeStep}
            setActiveStep={setActiveStep}
        />
    );
}

