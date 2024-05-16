import React, {useEffect, useState} from "react";
import {uploadForPreview} from "../../api/DjangoAPI";
import {InformationTextField} from "../algo_selection_components/InformationTextField";
import {DataSelectionComponent} from "../algo_selection_components/DataSelectionComponent";
import {PreprocessorSchema} from "../algo_selection_components/PreprocessorSchema";
import {StepperDialog} from "./StepperDialog";

import {TrainDataPreviewComplete, TSDConfig, MlConfig} from "../../typedefs/django_types";
// TODO try to use this instead of single implementations!
interface GenerateDataDialogProps {
    steps: Array<string>
    id: string,
    keepMounted: boolean,
    value: TSDConfig | MlConfig,
    open: boolean,
    isEdit: boolean,
    onClose: (value?: TSDConfig | MlConfig) => void
    onUpdateRefresh: () => void;
    handleCreate: () => void;
}

const set_initial_data = (value: TSDConfig | MlConfig) => {
    return {
        min_length: value.min_length,
        Imputation_Algorithm: value.imputation_algorithm?.name,
        "Processor Type": value.processing?.typeName
    }
}

export const GenerateDataDialog = (props: GenerateDataDialogProps) => {

    const {onClose, value: valueProp, open, isEdit, onUpdateRefresh, steps, handleCreate} = props;
    const [value, setValue] = useState(valueProp);

    const [selectedFiles, setSelectedFiles] = React.useState<File[]>([]);
    const [selectedItems, setSelectedItems] = React.useState<number[]>([]);
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
        const id = selectedItems.length !== 0 ? selectedItems[0] : -1
        //return uploadForPreview(selectedFiles, dataSetFormState.formData, id).then(res => {
        //    setTrainDataPreview(res)
        //});
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