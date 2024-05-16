import {Box, Button, Step, StepLabel, Stepper} from '@mui/material';
import React, {useMemo, useState} from 'react';
import {
    createDataSet,
    editDataSet,
    getDataSet,
    getDataTypeByName, getMlModelsWithConfiguration,
    getTSDModels, getTSDModelsWithConfiguration,
} from "../../../../../../api/SpringAPI";
import {DataSetFormState, DataType, TrainDataDTO, TSADataSet} from "../../../../../../typedefs/spring_types";
import {Stack} from "@mui/system";
import {SelectTrainDataStep} from "../steps/SelectTrainingDataStep";
import {InputForms, Model, TSDConfig} from "../../../../../../typedefs/django_types";
import {getTSDConfigByModelId} from "../../../../../../api/DjangoAPI";
import {useSnackbar} from "../../../../../shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../../../../../../typedefs/error_types";
import {DataSetFormStep} from "../steps/DataSetFormStep";
import {SelectConfigurationStep} from "../steps/SelectConfigurationStep";
import {SelectModelStep} from "../steps/SelectModelStep";
import {useTranslation} from "react-i18next";

interface props {
    dialogData: { dataSetId: number | null, projectId: number, trackId: number },
    onClose: () => void,
    open: boolean,
}

export const CreateTSADataSet = (props: props) => {
    const {dialogData, onClose, open} = props;

    const [tsaData, setTsaData] = useState<TSADataSet | null>(null);
    const [selectedModel, setSelectedModel] = useState<Model | null>(null);
    const [selectedConfig, setSelectedConfig] = useState<TSDConfig | null>(null);
    const [selectedTrainData, setSelectedTrainData] = useState<Array<TrainDataDTO>>([]);
    const {showMessage} = useSnackbar();
    const [activeStep, setActiveStep] = React.useState(0);
    const [allOffsets, setAllOffsets] = useState<{ [step: number]: { [key: string]: number } }>({});
    const [submitButtonEnabled, setSubmitButtonEnabled] = useState<boolean>(false);
    const [inputForm, setInputForm] = useState<InputForms | null>(null)
    const {t} = useTranslation(['dialogs', 'headers']);
    const [dataSetFormState, setDataSetFormState] = useState<DataSetFormState>(
        {
            ready: false,
            formData: {}
        }
    );

    const steps = ["select algorithm", "select configuration", "select train data", "set run values"]

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

    async function initStateFromAPI() {
        try {
            if (dialogData.dataSetId != null) {
                const loadedData = await getDataSet(dialogData.projectId, dialogData.trackId, dialogData.dataSetId) as TSADataSet;
                setDataSetFormState(() => ({
                    formData: loadedData,
                    ready: true,
                    type: DataType.TSA.valueOf().toLowerCase(),
                    dataType: DataType.TSA,
                }));
                setTsaData(loadedData);
            }
        } catch (error) {
            console.error("An error occurred while fetching the data: ", error);
        }
    }

    const onFormSubmit = () => {
        let data = JSON.parse(JSON.stringify(dataSetFormState.formData));
        data.type = DataType.TSA.valueOf().toLowerCase()
        data.dataType = DataType.TSA
        data.configurationId = selectedConfig?.id
        data.configs = selectedTrainData.map((selected, index) => {
            return {
                trainDataId: selected.id,
                level_configs: allOffsets[index]
            }
        })

        const operation = dialogData.dataSetId === null ? createDataSet : editDataSet;
        operation(data, dialogData.projectId, dialogData.trackId, dialogData.dataSetId!).then(() => {
            onClose();
        });
    }

    const renderStepContent = (stepIndex: number) => {
        switch (stepIndex) {
            case 0:
                return <SelectModelStep
                    selectedModel={selectedModel}
                    setSelectedModel={data => setSelectedModel(data)}
                    oldModelId={tsaData?.modelId} fetchData={getTSDModelsWithConfiguration}/>;
            case 1:
                return <SelectConfigurationStep
                    modelId={selectedModel!.id}
                    selectedConfig={selectedConfig}
                    setSelectedConfig={data => setSelectedConfig(data)}
                    oldModelId={tsaData?.configurationId}
                    fetchData={() => getTSDConfigByModelId(selectedModel!.id)}/>;
            case 2:
                return <SelectTrainDataStep
                    allOffsets={tsaData ? tsaData.configs.map(temp => temp.level_configs) : allOffsets}
                    setAllOffsets={setAllOffsets}
                    selectedTrainData={selectedTrainData}
                    setSelectedTrainData={setSelectedTrainData}
                    selectedConfigurationId={selectedConfig!.id}
                    selectedModelId={selectedModel!.id}
                    oldTrainingData={tsaData?.configs.map(temp => temp.trainDataId)}
                />;
            case 3:
                return <DataSetFormStep
                    onFormSubmit={onFormSubmit}
                    onSubmitButtonEnabled={setSubmitButtonEnabled}
                    dataSetFormState={dataSetFormState}
                    setDataSetFormState={setDataSetFormState}
                    inputForm={inputForm!}
                />;
            default:
                return <div>Unknown step</div>;
        }
    };


    useMemo(() => {
        initStateFromAPI().then();
        getDataTypeByName(DataType.TSA.valueOf()).then(async res => {
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
    )
}