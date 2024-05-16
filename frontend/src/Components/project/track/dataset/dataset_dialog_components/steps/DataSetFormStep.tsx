import React, {useEffect} from "react";
import {DataSetFormState} from "../../../../../../typedefs/spring_types";
import {DataSetFormComponent} from "../../skeletons/DataSetFormComponent";
import {InputForms} from "../../../../../../typedefs/django_types";


interface FormStateProps {
    onFormSubmit: (data: DataSetFormState) => void;
    onSubmitButtonEnabled: (enabled: boolean) => void;
    dataSetFormState: DataSetFormState;
    setDataSetFormState: (data: (oldState: any) => any) => void;
    inputForm?: InputForms;
}


export const DataSetFormStep = (props: FormStateProps) => {
    const {onFormSubmit, dataSetFormState, setDataSetFormState, onSubmitButtonEnabled, inputForm} = props;

    const onFormDataChanged = (errors: any, data: any) => {

        const hasErrors = errors.length > 0;
        onSubmitButtonEnabled(!hasErrors);

        // TODO: error handling
        setDataSetFormState((oldState) => ({
            ...oldState,
            formData: data
        }));
    }


    async function updateFormSchema() {
        let newFormSchema = JSON.parse(JSON.stringify(inputForm?.schema));
    }

    useEffect(() => {
        updateFormSchema().then()
    }, []);
    return (
        inputForm ?
            <DataSetFormComponent
                schema={inputForm}
                dataSetFormState={dataSetFormState}
                onFormDataChanged={onFormDataChanged}
                onCancel={() => console.log("closing")}
                onFormSubmit={() => onFormSubmit(dataSetFormState)}
            />
            : null
    );
};