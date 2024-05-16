import React, {useEffect, useState} from 'react';
import {InputForms, TrainDataPreviewComplete} from '../../typedefs/django_types';
import {getProcessingSchema} from '../../api/DjangoAPI';
import {Accordion, AccordionDetails, AccordionSummary, Container} from '@mui/material';
import PreprocessPreviewGraph from "../graphs/PreprocessPreviewGraph";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import {DataSetFormComponent} from "../project/track/dataset/skeletons/DataSetFormComponent";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";

interface SolutionCardsProps {
    postPreview: (preprocessorName: string) => void;
    data?: TrainDataPreviewComplete;
    isPreprocessorValid: (isEnabled: boolean) => void;
}

interface DataFormState {
    dataSetFormState: any;
    setDataSetFormState: React.Dispatch<React.SetStateAction<any>>;
}


interface PreprocessorSchemaProps extends SolutionCardsProps, DataFormState {
}

export const PreprocessorSchema = (props: PreprocessorSchemaProps) => {
    const [inputForm, setInputForm] = useState<InputForms | null>(null)
    const [activeStep, setActiveStep] = useState<number>(0);


    const onFormDataChanged = (errors: any, data: any) => {
        const hasErrors = errors.length > 0;
        props.setDataSetFormState((oldState: any) => ({
            ...oldState,
            formData: data
        }));
    }

    useEffect(() => {
        console.log(props.dataSetFormState)
        getProcessingSchema().then(res => {
            setInputForm(res as InputForms)
        })
    }, [setInputForm]);


    const getJsonSchema = () => {
        return inputForm ? (
            <DataSetFormComponent
                schema={inputForm}
                dataSetFormState={props.dataSetFormState}
                onFormDataChanged={onFormDataChanged}
                onCancel={handleCancel}
                onFormSubmit={onFormSubmit}/>
        ) : null;
    }


    const handleCancel = () => {
        props.setDataSetFormState({})
    }

    const onFormSubmit = () => {

    }


    const getData = async () => {
        props.postPreview(props.dataSetFormState["Processor Type"]);
        setActiveStep(1)
    }

    const getPreview = () => {
        return <div>
            {props.data
                ? <PreprocessPreviewGraph
                    data={props.data.original}
                    processed_data={props.data.preview}
                    flags={props.data.flags}/>
                : null}
        </div>;
    }

    return (
        <div>
            <Container>
                <Accordion expanded={activeStep === 0}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon/>}
                        onClick={() => setActiveStep(0)}
                    >
                        Select Parameter
                    </AccordionSummary>
                    <AccordionDetails>
                        {getJsonSchema()}
                    </AccordionDetails>
                </Accordion>
                <Accordion expanded={activeStep === 1}>
                    <AccordionSummary
                        expandIcon={<ExpandMoreIcon/>}
                        onClick={() => getData()}
                    >
                        Preview
                    </AccordionSummary>
                    <AccordionDetails>
                        {getPreview()}
                    </AccordionDetails>
                </Accordion>
            </Container>
        </div>
    );
};
