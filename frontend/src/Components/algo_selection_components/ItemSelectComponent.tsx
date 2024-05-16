import React, {useEffect, useState} from "react";
import {TrainingData, TrainingDataFiles} from "../../typedefs/django_types";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import {TrainingDataItemSelect} from "./TrainingDataItemSelect";
import {TrainingDataFileSelect} from "./TrainDataFileSelect";
import {Box} from "@mui/material";
import {useTranslation} from "react-i18next";

interface DataSelectProps {
    selectedItems: number[];
    setSelectedItems: React.Dispatch<React.SetStateAction<number[]>>;
    trainingDataSets: Array<TrainingData>;

    selectedFiles: number[];
    setSelectedFiles: React.Dispatch<React.SetStateAction<number[]>>;
    trainingDataFiles: Array<TrainingDataFiles>;
}

export const ItemSelectComponent = (props: DataSelectProps) => {
    const {t} = useTranslation(['headers']);

    const {
        selectedItems,
        setSelectedItems,
        trainingDataSets,
        selectedFiles,
        setSelectedFiles,
        trainingDataFiles
    } = props;
    const [activeTab, setActiveTab] = useState(0)
    const handleChangeTab = (event: any, newValue: any) => {
        setActiveTab(newValue);
    };

    useEffect(() => {

    }, [trainingDataSets, trainingDataFiles, selectedItems, selectedFiles]);

    return (
        <Box sx={{width: '90%', mb: 2, mt: 2}}>
            <Tabs value={activeTab}
                  onChange={handleChangeTab}
                  variant="fullWidth"
                  aria-label="login-signup-tabs"
                  sx={{mb: 2}}>
                <Tab label={t('select_files', {ns: ['headers']})}/>
                <Tab label={t('select_items', {ns: ['headers']})}/>
            </Tabs>

            {activeTab === 0
                ? <TrainingDataFileSelect
                    selectedItems={selectedFiles}
                    setSelectedFiles={setSelectedFiles}
                    trainingDataFiles={trainingDataFiles}/>
                : <TrainingDataItemSelect
                    selectedItems={selectedItems}
                    setSelectedItems={setSelectedItems}
                    trainingDataSets={trainingDataSets}/>
            }
        </Box>
    );
}