import React from 'react';
import {useDropzone} from 'react-dropzone';
import {useTranslation} from "react-i18next";

interface FileDropzoneProps {
    onDrop: (acceptedFiles: File[]) => void;
}

export const FileDropzone: React.FC<FileDropzoneProps> = ({onDrop}) => {
    const {getRootProps, getInputProps} = useDropzone({onDrop, multiple: true});
    const { t } = useTranslation(['dialogs']);
    return (
        <div {...getRootProps()} style={{
            border: '2px dashed gray',
            padding: '10px',
            borderRadius: '4px',
            cursor: 'pointer',
            textAlign: 'center',
            minHeight: '25vh'
        }}>
            <input {...getInputProps()} />
            <p>{t('dialog_set_information_drag_n_drop_train_data', {ns: ['dialogs']})}</p>
        </div>
    );
};