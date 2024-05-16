import React, {useMemo, useState} from "react";
import {getUserFiles} from "../api/DjangoAPI";
import {TrainingDataFiles} from "../typedefs/django_types";
import GenericAccordion from "../Components/shared_components/GenericAccordion";
import {Grid} from "@mui/material";
import {PaperContainerComponent} from "../Components/shared_components/paper/PaperComponent";
import {ElementCardComponent} from "../Components/shared_components/cards/ElementCardComponent";
import {ListDataSetComponents} from "../Components/dataview/ListDataSetComponents";
import {SearchBarComponent} from "../Components/shared_components/SearchBarComponent";
import {DataUploadDialog} from "../Components/dialogs/DataUploadDialog";
import {useTranslation} from "react-i18next";
import {NewElementButton} from "../Components/buttons/NewElementButton";

export const DataSetViewer = () => {
    const [trainingDataFiles, setTrainingDataFiles] = useState<Array<TrainingDataFiles>>([])
    const [expandID, setExpandId] = useState<number | null>(null)
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [selectedFiles, setSelectedFiles] = useState<Array<TrainingDataFiles>>([]);
    const [openDialog, setOpenDialog] = useState(false)
    const {t} = useTranslation(['dialogs', 'headers']);

    const handleSearchQuery = (event: React.ChangeEvent<HTMLInputElement>) => {
        setSearchQuery(event.target.value);
        if (event.target.value !== "") {
            setSelectedFiles(trainingDataFiles.filter(file => file.name.startsWith(event.target.value)));
        } else {
            setSelectedFiles(trainingDataFiles);
        }
    };

    const onClose = () => {
        setOpenDialog(false)
        refreshConfigs()
    }

    const refreshConfigs = () => {
        getUserFiles().then(res => {
            setTrainingDataFiles(res)
            setSelectedFiles(res)
        })
    };

    useMemo(() => {
        getUserFiles().then(res => {
            setTrainingDataFiles(res)
            setSelectedFiles(res)
        })
    }, []);


    return <>
        <PaperContainerComponent>
            <ElementCardComponent header={t("data_header", {ns: ['headers']})}>
                <SearchBarComponent searchQuery={searchQuery} handleSearchQuery={handleSearchQuery}/>
                {selectedFiles && selectedFiles.length > 0
                    ? selectedFiles.map((config) => (
                        <Grid key={config.id} item xs={1}>
                            <GenericAccordion
                                expanded={config.id === expandID}
                                onChange={() => setExpandId(expandID === config.id ? null : config.id)}
                                details={
                                    <ListDataSetComponents fileId={config.id} onRefresh={refreshConfigs}/>
                                }
                                header={config.name}
                            />
                        </Grid>
                    ))
                    : null}
                <NewElementButton message={"Create new ML Configuration"} handleClick={() => setOpenDialog(true)}/>
            </ElementCardComponent>
            <DataUploadDialog
                open={openDialog}
                onClose={onClose}/>
        </PaperContainerComponent>
    </>

}