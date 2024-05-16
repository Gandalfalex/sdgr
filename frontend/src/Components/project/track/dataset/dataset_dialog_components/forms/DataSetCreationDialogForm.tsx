import React, {useEffect, useState} from "react";
import {InputForms} from "../../../../../../typedefs/django_types";
import {DataSetFormState, DataType} from "../../../../../../typedefs/spring_types";
import {createDataSet, editDataSet, getDataSet, getDataTypeByName} from "../../../../../../api/SpringAPI";
import {Button, Container} from "@mui/material";
import {DataSetFormComponent} from "../../skeletons/DataSetFormComponent";
import {useTranslation} from "react-i18next";
import {getDataType} from "../../elements/DataSetHOC";

interface DataSetProps {
    dialogData: { dataSetId: number | null, projectId: number, trackId: number };
    onClose: () => void;
    open: boolean;
    dataType: DataType;
}

export const DataSetCreationDialogForm = (props: DataSetProps) => {
    const {dialogData, onClose, open} = props;
    const [submitButtonEnabled, setSubmitButtonEnabled] = useState<boolean>(false);
    const {t} = useTranslation(['dialogs']);
    const [inputForm, setInputForm] = useState<InputForms | null>(null)
    const [storedForms, setStoredForms] = useState<Record<string, InputForms>>({});
    const [dataSetFormState, setDataSetFormState] = useState<DataSetFormState>(
        {
            ready: false,
            formData: {}
        }
    );

    async function initStateFromAPI() {
        try {
            if (dialogData.dataSetId != null) {
                getDataSet(dialogData.projectId, dialogData.trackId, dialogData.dataSetId).then(res => {
                    setDataSetFormState(() => ({
                        formData: getDataType(props.dataType, res),
                        ready: true,
                    }))
                })
            }
        } catch (error) {
            console.error("An error occurred while fetching the data: ", error);
        }
    }

    const onFormDataChanged = (errors: any, data: any) => {
        const hasErrors = errors.length > 0;
        setSubmitButtonEnabled(!hasErrors);

        setDataSetFormState((oldState) => ({
            ...oldState,
            formData: data
        }));
    }

    const onFormSubmit = () => {
        let data = JSON.parse(JSON.stringify(dataSetFormState.formData));
        data.type = props.dataType.valueOf().toLowerCase()
        data.dataType = props.dataType

        if (props.dataType === DataType.FLOAT || props.dataType === DataType.INTEGER) {
            data = processFloatIntegerData(data);
        }

        const operation = dialogData.dataSetId === null ? createDataSet : editDataSet;
        operation(data, dialogData.projectId, dialogData.trackId, dialogData.dataSetId!).then(() => {
            onClose();
        });
    }

    const processFloatIntegerData = (data: any) => {
        data.trendOption = data.trendOption || {};
        data.seasonOption = data.seasonOption || {};
        data.residualOption = data.residualOption || {};

        data.trendOption.type = data.trend;
        data.seasonOption.type = data.season;
        data.residualOption.type = data.residual;
        return data;
    }

    const onCancel = () => {
        onClose();
    }

    useEffect(() => {
        if (!storedForms[props.dataType]) {
            initStateFromAPI().then();
            getDataTypeByName(props.dataType.valueOf()).then(async res => {
                setStoredForms(prevForms => ({...prevForms, [props.dataType]: res}));
                setInputForm(res);
            })
        } else {
            setInputForm(storedForms[props.dataType]);
        }
    }, [open, props.dataType]);
    return (
        inputForm
            ? <Container>
                <DataSetFormComponent
                    schema={inputForm}
                    dataSetFormState={dataSetFormState}
                    onFormDataChanged={onFormDataChanged}
                    onCancel={onCancel}
                    onFormSubmit={onFormSubmit}/>
                <Button onClick={onCancel}>{t('button_label.cancel', {ns: ['dialogs']})} </Button>
                <Button onClick={onFormSubmit}
                        disabled={!submitButtonEnabled}> {t('button_label.send', {ns: ['dialogs']})} </Button>
            </Container>
            : null
    )
}