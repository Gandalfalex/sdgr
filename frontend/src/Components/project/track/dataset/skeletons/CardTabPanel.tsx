import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import TabPanel from "@mui/lab/TabPanel";
import {Box, Grid, IconButton, Tooltip, useTheme} from "@mui/material";
import {DragDropContext, Draggable, Droppable} from "react-beautiful-dnd";
import {DataSet, DataSetDialogData, DataType, Track} from "../../../../../typedefs/spring_types";
import AddIcon from "@mui/icons-material/Add";
import React, {SyntheticEvent, useEffect, useState} from "react";
import {TabContext} from "@mui/lab";
import {LogGraphChooserElement} from "../../LogGraphChooserElement";
import {LogMessageElement} from "../../LogMessageElement";
import {editDataSet, getAllDataSets} from "../../../../../api/SpringAPI";
import {
    DataSetTypeMap,
} from "../elements/DataSetHOC";
import {DataTypeSelection} from "../dataset_dialog_components/DataSetTypeSelection";
import {useTranslation} from "react-i18next";


interface TrackPanelProps {
    projectId: number;
    track: Track;
    refreshTracks: () => void
}


const CardTabPanel: React.FC<TrackPanelProps> = ({projectId, track, refreshTracks}) => {
    const [value, setValue] = useState('dataSets');
    const [dataSets, setAllDataSets] = useState<Array<DataSet>>([]);
    const [openCreateDataSetDialog, setOpenCreateDataSetDialog] = useState<boolean>(false);
    const { t } = useTranslation(['dialogs', 'components']);
    const theme = useTheme();

    const [dataSetDialogData, setDataSetDialogData] = useState<DataSetDialogData>(
        {
            dataSetId: null,
            trackId: track.id,
            projectId: projectId
        }
    );


    const handleChange = (event: SyntheticEvent, newValue: string) => {
        setValue(newValue);
    };

    const onEditDataSet = (dataSetId: number) => {
        setDataSetDialogData({...dataSetDialogData, dataSetId: dataSetId});
        setOpenCreateDataSetDialog(true);
    }
    const refreshDataSets = () => {
        getAllDataSets(projectId, track.id).then(res => {
                setAllDataSets(res);
            }
        );
    }
    const handleNewDataSet = () => {
        setOpenCreateDataSetDialog(true);
    }

    const reorder = (list: Array<DataSet>, startIndex: number, endIndex: number) => {
        const result = Array.from(list);
        const [removed] = result.splice(startIndex, 1);
        result.splice(endIndex, 0, removed);

        return result;
    };

    const getListStyle = (isDraggingOver: boolean) => ({
        background: isDraggingOver ? 'lightblue' : theme.palette.secondary.light,
        display: 'flex',
        padding: 6,
        gap: 4,
        overflow: 'auto',
    });

    const handleCloseDataSet = () => {
        setDataSetDialogData({...dataSetDialogData, dataSetId: null});
        setOpenCreateDataSetDialog(false);
        refreshDataSets();
    }

    const onDragEnd = (e: any) => {
        setAllDataSets((oldState) => {
            const reorderedDataSets = reorder(oldState, e.source.index, e.destination.index);
            if (e.source.index !== e.destination.index) {
                dataSets[e.source.index].position = e.destination.index;
                editDataSet(reorderedDataSets[e.destination.index], projectId, track.id, e.draggableId)
                    .then(() => {
                        return getAllDataSets(projectId, track.id)
                    })
                    .then((response) => {
                        setAllDataSets(response);
                    })
                    .catch((error) => {
                        console.error("An error occurred while fetching datasets: ", error);
                    });
            }
            return reorderedDataSets;

        })
    }

    useEffect(() => {
        getAllDataSets(projectId, track.id).then(res => {
            return setAllDataSets(res);
        });
    }, [])
    return (
        <Box sx={{display: 'flex', width: "100vw"}}>
            <TabContext value={value}>
                <Tabs
                    orientation="vertical"

                    value={value}
                    onChange={handleChange}
                    aria-label="Vertical tabs example"
                    sx={{borderRight: 1, borderColor: 'divider', width: "7%"}}
                >
                    <Tab value="dataSets"   label={t('data_set_datasets', {ns: ['components']})} wrapped/>
                    <Tab value="Logs"       label={t('data_set_logs', {ns: ['components']})} wrapped/>
                    <Tab value="Graph"      label={t('data_set_graph', {ns: ['components']})} wrapped/>
                </Tabs>
                <TabPanel value="dataSets" sx={{overflow: "hidden", width: "93%"}}>
                    <Grid container wrap="nowrap"
                          direction="row"
                          justifyContent="flex-start"
                          alignItems="stretch"
                          paddingBottom={1}
                    >
                        <DragDropContext onDragEnd={onDragEnd}>
                            <Droppable droppableId={String(track.id)} direction="horizontal">
                                {(provided, snapshot) => {
                                    return (<div
                                        ref={provided.innerRef}
                                        style={getListStyle(snapshot.isDraggingOver)}
                                        {...provided.droppableProps}
                                    >
                                        {dataSets.map((dataSet, index) => {
                                            return (
                                                <Draggable key={String(dataSet.id)} draggableId={String(dataSet.id)}
                                                           index={index}>
                                                    {(provided) => (
                                                        <div
                                                            ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
                                                            {(() => {
                                                                const DataSetComponent = DataSetTypeMap[dataSet.dataType];
                                                                return (
                                                                    <DataSetComponent
                                                                        key={dataSet.id}
                                                                        projectId={projectId}
                                                                        trackId={track.id}
                                                                        dataSet={dataSet}
                                                                        updateDataSet={refreshDataSets}
                                                                        onEditDataSet={onEditDataSet}
                                                                    />
                                                                );
                                                            })()}
                                                        </div>
                                                    )}
                                                </Draggable>
                                            );
                                        })}
                                        {provided.placeholder}
                                        <Box sx={{
                                            height: "380px",
                                            width: "300px",
                                            maxWidth: "80vw",
                                            display: 'flex',
                                            alignSelf: "center",
                                            justifyContent: 'center'
                                        }}>
                                            <Tooltip title={t('new_data_set', {ns: ['dialogs']})} arrow>
                                                <IconButton className={'growButton'} onClick={handleNewDataSet}
                                                            sx={{
                                                                color: theme.palette.primary.main,
                                                                alignSelf: 'center',
                                                            }}>
                                                    <AddIcon sx={{
                                                        fontSize: 'xx-large'
                                                    }}/>
                                                </IconButton>
                                            </Tooltip>
                                        </Box>
                                    </div>);
                                }}
                            </Droppable>
                        </DragDropContext>
                    </Grid>
                </TabPanel>
                <TabPanel value="Logs" sx={{width: "93%"}}>
                    <Grid container gap={2} wrap="nowrap"
                          direction="column"
                          justifyContent="flex-start"
                          alignItems="center" sx={{height: "100%", width: '100%', p: 1, pt: 0}}>
                        <Grid key={track.id} item xs={1}>
                            <LogMessageElement trackId={track.id}/>
                        </Grid>
                    </Grid>
                </TabPanel>
                <TabPanel value="Graph" sx={{width: "93%"}}>
                    <LogGraphChooserElement trackId={track.id}/>
                </TabPanel>
            </TabContext>

            <DataTypeSelection
                dialogData={dataSetDialogData}
                onClose={handleCloseDataSet}
                open={openCreateDataSetDialog}
                allowed_types={track.allowedDataTypes}/>

        </Box>
    )
}

export default CardTabPanel;