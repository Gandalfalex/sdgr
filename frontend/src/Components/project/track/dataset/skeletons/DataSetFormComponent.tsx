import React, {useEffect, useState} from 'react';
import {DataSetFormState} from "../../../../../typedefs/spring_types";
import Form from '@rjsf/mui';
import validator from '@rjsf/validator-ajv8';
import {IChangeEvent} from "@rjsf/core";
import {InputForms} from "../../../../../typedefs/django_types";

import '../../../../../css/tsrordering.css';
import {useTranslation} from "react-i18next";
import {useErrorMessageConverter} from "../../../../translation_rsjf/ErrorMessageTranslator";
import {translateSchema} from "../../../../translation_rsjf/SchemaTranslator";

interface DataSetFormComponentProps {
    schema: InputForms
    dataSetFormState: DataSetFormState | any;
    onFormDataChanged: (errors: any, data: any) => void;
    onCancel: () => void;
    onFormSubmit: () => void;
}


export const DataSetFormComponent: React.FC<DataSetFormComponentProps> = ({
                                                                              schema,
                                                                              dataSetFormState,
                                                                              onFormDataChanged,
                                                                              onFormSubmit,
                                                                              onCancel
                                                                          }) => {

    const {t} = useTranslation(['schemas']);
    const [translatedSchema, setTranslatedSchema] = useState<InputForms>();
    const convertError = useErrorMessageConverter();

    const handleChange = (e: IChangeEvent<any>) => {
        onFormDataChanged(e.errors, e.formData);
    };


    const handleSubmit = (e: IChangeEvent<any>) => {
        if (e.errors.length === 0) {
            onFormSubmit();
        } else {
            onCancel();
        }
    };

    function transformErrors(errors: any[], uiSchema: any) {
        return errors.map((error) => {
            error.message = convertError(error)
            return error;
        });
    }


    useEffect(() => {
        if (schema) setTranslatedSchema(translateSchema(schema, t));
        console.log(translatedSchema?.schema)
    }, [schema, t]);

    return (
        <div>
            {translatedSchema ?
                <Form
                    schema={translatedSchema.schema}
                    uiSchema={translatedSchema.ui_schema}
                    formData={dataSetFormState.formData}
                    onChange={handleChange}
                    onSubmit={handleSubmit}
                    transformErrors={transformErrors}
                    validator={validator}
                    liveValidate={true}
                    noHtml5Validate={true}
                    showErrorList={false}
                    className="my-custom-form"
                />
                : null
            }
        </div>
    );
};