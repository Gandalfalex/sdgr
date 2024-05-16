import {Typography} from "@mui/material";
import {ItemSelectComponent} from "./ItemSelectComponent";
import {FileDropzone} from "./FileDropZone";
import {ListItemSection} from "./ListItemSelection";
import React, {useEffect, useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import {getAllTrainingData, getUserFiles} from "../../api/DjangoAPI";
import {TrainingData, TrainingDataFiles} from "../../typedefs/django_types";

interface ItemProps {
    selectedItems: number[];
    setSelectedItems: React.Dispatch<React.SetStateAction<number[]>>;
    selectedTrainFiles: number[];
    setSelectedTrainFiles: React.Dispatch<React.SetStateAction<number[]>>;
    selectedFiles: File[];
    setSelectedFiles: React.Dispatch<React.SetStateAction<File[]>>;
}

export const DataSelectionComponent = (props: ItemProps) => {
    const {
        selectedItems,
        setSelectedItems,
        selectedTrainFiles,
        setSelectedTrainFiles,
        selectedFiles,
        setSelectedFiles
    } = props;

    const [trainingDataSets, setTrainingDataSets] = useState<Array<TrainingData>>([])
    const [trainingDataFiles, setTrainingDataFiles] = useState<Array<TrainingDataFiles>>([])

    const onDrop = React.useCallback((acceptedFiles: File[]) => {
        setSelectedFiles(acceptedFiles);
    }, []);

    const {t} = useTranslation(['dialogs', 'headers']);


    useMemo(() => {
        getAllTrainingData("false").then(res => setTrainingDataSets(res))
        getUserFiles().then(res => setTrainingDataFiles(res))
    }, []);

    useEffect(() => {
    }, [selectedItems, selectedTrainFiles, selectedFiles]);

    return (
        <div>
            <Typography>
                {t('dialog_set_information_choose_train_data', {ns: ['dialogs']})}
            </Typography>
            <ItemSelectComponent
                selectedItems={selectedItems}
                setSelectedItems={setSelectedItems}
                trainingDataSets={trainingDataSets}
                selectedFiles={selectedTrainFiles}
                setSelectedFiles={setSelectedTrainFiles}
                trainingDataFiles={trainingDataFiles}
            />

            <FileDropzone
                onDrop={onDrop}/>
            <ListItemSection
                selectedItems={selectedItems}
                selectedFiles={selectedFiles}
                trainingDataSets={trainingDataSets}
                setSelectedItems={setSelectedItems}
                setSelectedFiles={setSelectedFiles}
                selectedTrainingDataFiles={selectedTrainFiles}
                trainingDataSetFiles={trainingDataFiles}
                setSelectedTrainingDataFiles={setSelectedTrainFiles}/>
        </div>);
}