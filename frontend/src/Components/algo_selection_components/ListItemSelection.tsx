import React from 'react';
import DeleteIcon from '@mui/icons-material/Delete';
import {TrainingData, TrainingDataFiles} from "../../typedefs/django_types";

export interface ListItemSectionProps {
    selectedItems?: number[];
    trainingDataSets: Array<TrainingData>;
    setSelectedItems?: React.Dispatch<React.SetStateAction<number[]>>;

    trainingDataSetFiles: Array<TrainingDataFiles>;
    selectedTrainingDataFiles: number[];
    setSelectedTrainingDataFiles?: React.Dispatch<React.SetStateAction<number[]>>;


    selectedFiles: File[];
    setSelectedFiles: React.Dispatch<React.SetStateAction<File[]>>;
}

export const ListItemSection: React.FC<ListItemSectionProps> = ({
                                                                    selectedItems,
                                                                    selectedFiles,
                                                                    trainingDataSets,
                                                                    setSelectedItems,
                                                                    setSelectedFiles,
                                                                    selectedTrainingDataFiles,
                                                                    trainingDataSetFiles,
                                                                    setSelectedTrainingDataFiles
                                                                }) => (
    <ul style={{width: '90%'}}>

        {selectedItems ?
            selectedItems.map((itemId, index) => {
                const item = trainingDataSets.find(data => data.id === itemId);
                if (!item) return null; // Safety check
                return (
                    <li key={itemId}
                        style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%'}}>
                        Selected item: {item.name}
                        <DeleteIcon style={{cursor: 'pointer', marginLeft: '10px'}} onClick={() => {
                            const updatedItems = [...selectedItems];
                            updatedItems.splice(index, 1);
                            setSelectedItems!(updatedItems);
                        }}/>
                    </li>
                );
            }) : null}
        {selectedTrainingDataFiles ?
            selectedTrainingDataFiles.map((itemId, index) => {
                const item = trainingDataSetFiles.find(data => data.id === itemId);
                if (!item) return null; // Safety check
                return (
                    <li key={itemId}
                        style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%'}}>
                        Selected item: {item.name}
                        <DeleteIcon style={{cursor: 'pointer', marginLeft: '10px'}} onClick={() => {
                            const updatedItems = [...selectedTrainingDataFiles];
                            updatedItems.splice(index, 1);
                            setSelectedTrainingDataFiles!(updatedItems);
                        }}/>
                    </li>
                );
            }) : null}
        {selectedFiles.map((file, index) => (
            <li key={file.name}
                style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', width: '100%'}}>
                Selected file: {file.name}
                <DeleteIcon style={{cursor: 'pointer', marginLeft: '10px'}} onClick={() => {
                    const updatedFiles = [...selectedFiles];
                    updatedFiles.splice(index, 1);
                    setSelectedFiles(updatedFiles);
                }}/>
            </li>
        ))}
    </ul>
);