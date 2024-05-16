import {Box, Button, Step, StepLabel, Stepper} from '@mui/material';
import React, {useMemo, useState} from 'react';
import {
    createDataSet,
    editDataSet,
    getDataSet,
    getDataTypeByName,
    getMlConfigurationsByModelId,
    getMlModels, getMlModelsWithConfiguration,
} from "../../../../../../api/SpringAPI";
import {DataSetFormState, DataType, MLDataSet} from "../../../../../../typedefs/spring_types";
import {Stack} from "@mui/system";
import {InputForms, MlConfig, Model} from "../../../../../../typedefs/django_types";
import {SnackbarSeverity} from "../../../../../../typedefs/error_types";
import {useSnackbar} from "../../../../../shared_components/snackbar/SnackbarContext";
import {DataSetFormStep} from "../steps/DataSetFormStep";
import {SelectConfigurationStep} from "../steps/SelectConfigurationStep";
import {SelectModelStep} from "../steps/SelectModelStep";
import {useTranslation} from "react-i18next";


interface props {
    dialogData: { dataSetId: number | null, projectId: number, trackId: number },
    onClose: () => void,
    open: boolean,
}

export const CreateMLDataSet = (props: props) => {
    const {dialogData, onClose, open} = props;

    const [mlData, setMlData] = useState<MLDataSet | null>(null);
    const [activeStep, setActiveStep] = React.useState(0);
    const [selectedModel, setSelectedModel] = useState<Model | null>(null);
    const [selectedConfig, setSelectedConfig] = useState<MlConfig | null>(null);
    const steps = ["select algorithm", "select configuration", "set run values"]
    const [submitButtonEnabled, setSubmitButtonEnabled] = useState<boolean>(false);
    const [inputForm, setInputForm] = useState<InputForms | null>(null)
    const {showMessage} = useSnackbar();
    const {t} = useTranslation(['dialogs', 'headers']);

    const [dataSetFormState, setDataSetFormState] = useState<DataSetFormState>(
        {
            ready: false,
            formData: {}
        }
    );


    async function initStateFromAPI() {
        try {
            if (dialogData.dataSetId != null) {
                const loadedData = await getDataSet(dialogData.projectId, dialogData.trackId, dialogData.dataSetId) as MLDataSet;
                setDataSetFormState(() => ({
                    formData: loadedData,
                    ready: true,
                    type: DataType.ML.valueOf().toLowerCase(),
                    dataType: DataType.ML,
                    generation_option: "GENERATE"
                }));
                setMlData(loadedData);
            }
        } catch (error) {
            console.error("An error occurred while fetching the data: ", error);
        }
    }

    const onFormSubmit = () => {
        let data = JSON.parse(JSON.stringify(dataSetFormState.formData));
        data.type = DataType.ML.valueOf().toLowerCase()
        data.configurationId = selectedConfig?.id
        data.generation_option = "GENERATE"
        data.dataType = DataType.ML

        const operation = dialogData.dataSetId === null ? createDataSet : editDataSet;
        operation(data, dialogData.projectId, dialogData.trackId, dialogData.dataSetId!).then(() => {
            onClose();
        });
    }

    const handleNext = () => {
        if (activeStep === 0) {
            if (selectedModel) {
                setActiveStep((prevActiveStep) => prevActiveStep + 1);
            } else {
                showMessage(t('select_model_step_1', {ns: ['dialogs']}), SnackbarSeverity.WARNING);
            }
        } else if (activeStep === 1) {
            if (selectedConfig) {
                setActiveStep((prevActiveStep) => prevActiveStep + 1);
            } else {
                showMessage(t('select_model_step_2', {ns: ['dialogs']}), SnackbarSeverity.WARNING);
            }
        } else {
            setActiveStep((prevActiveStep) => prevActiveStep + 1);
        }
    };

    const handleBack = () => {
        if (activeStep === 0) {
            onClose();
        }
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };


    const renderStepContent = (stepIndex: number) => {
        switch (stepIndex) {
            case 0:
                return <SelectModelStep
                    selectedModel={selectedModel}
                    setSelectedModel={data => setSelectedModel(data)}
                    oldModelId={mlData?.modelId}
                    fetchData={getMlModelsWithConfiguration}/>;
            case 1:
                return <SelectConfigurationStep
                    modelId={selectedModel!.id}
                    selectedConfig={selectedConfig}
                    setSelectedConfig={data => {
                        setSelectedConfig(data)
                        dataSetFormState.formData.configurationId = data.id
                        getDataTypeByName(DataType.ML.valueOf(), {"configurationId": data?.id}).then(async res => {
                            setInputForm(res)
                        })
                    }}
                    oldModelId={mlData?.configurationId}
                    fetchData={() => getMlConfigurationsByModelId(selectedModel!.id)}/>;
            case 2:
                return <DataSetFormStep
                    onFormSubmit={onFormSubmit}
                    dataSetFormState={dataSetFormState}
                    setDataSetFormState={setDataSetFormState}
                    onSubmitButtonEnabled={setSubmitButtonEnabled}
                    inputForm={inputForm!}
                />;
            default:
                return <div>Unknown step</div>;
        }
    };


    useMemo(() => {
        initStateFromAPI().then();
        getDataTypeByName(DataType.ML.valueOf()).then(async res => {
            setInputForm(res)
        })
    }, [open]);
    return (
        <div>
            <Box display="flex" flexDirection="row">
                <Stack direction="row" spacing={2}>
                    <Stepper activeStep={activeStep} orientation="vertical">
                        {steps.map((label, index) => (
                            <Step key={label}>
                                <StepLabel>{label}</StepLabel>
                            </Step>
                        ))}
                    </Stepper>
                    <Box flexGrow={1} pl={2} pr={2}>
                        {renderStepContent(activeStep)}
                    </Box>
                </Stack>
            </Box>
            <Box display="flex" justifyContent="space-between" mt={2}>
                <Button
                    onClick={handleBack}> {activeStep === 0 ? t('button_label.cancel', {ns: ['dialogs']}) : t('button_label.back', {ns: ['dialogs']})} </Button>
                <Box>
                    {activeStep !== steps.length - 1 && (
                        <Button onClick={handleNext}
                                disabled={activeStep === steps.length - 1}> {t('button_label.next', {ns: ['dialogs']})} </Button>
                    )}
                    {activeStep === steps.length - 1 && (
                        <Button onClick={onFormSubmit}
                                disabled={!submitButtonEnabled}> {t('button_label.send', {ns: ['dialogs']})} </Button>
                    )}
                </Box>
            </Box>
        </div>
    );
}