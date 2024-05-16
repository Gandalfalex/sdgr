import React, {useEffect, useState} from 'react';
import {Dialog, DialogContent} from '@mui/material';
import {
    DataSet,
    DataSetDialogData,
    DataType,
    DataTypeSchema,
    GROUPS,
    GroupType
} from '../../../../../typedefs/spring_types';
import {CreateMLDataSet} from "./forms/MLDialogForm";
import {CreateTSADataSet} from "./forms/TSADialogForm";
import {DataSetCreationDialogForm} from "./forms/DataSetCreationDialogForm";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import {getDataSet} from "../../../../../api/SpringAPI";

interface SelectionDialogProps {
    open: boolean;
    onClose: () => void;
    dialogData: DataSetDialogData;
    allowed_types: Array<DataTypeSchema>;
}


export const DataTypeSelection: React.FC<SelectionDialogProps> = ({open, onClose, dialogData, allowed_types}) => {
    // @ts-ignore
    const [selectedGroup, setSelectedGroup] = useState<GroupType>(Object.keys(GROUPS)[0]);
    // @ts-ignore
    const [selectedDataType, setSelectedDataType] = useState<DataType>(GROUPS[Object.keys(GROUPS)[0]][0]);
    const [activeGroup, setActiveGroup] = useState<GroupType | null>(null);
    const [activeDataType, setActiveDataType] = useState(DataType.NONE)

    const handleDialogClose = () => {
        // @ts-ignore
        setSelectedGroup(Object.keys(GROUPS)[0]);
        setActiveGroup(null)
        onClose();
    };


    const renderDataContainer = () => {
        return getDataContainer(selectedDataType)
    };

    const getDataContainer = (dataType: DataType) => {
        switch (dataType) {
            case DataType.TSA:
                return <CreateTSADataSet
                    dialogData={dialogData}
                    onClose={handleDialogClose}
                    open={true}/>;
            case DataType.ML:
                return <CreateMLDataSet
                    dialogData={dialogData}
                    onClose={handleDialogClose}
                    open={true}/>;
            default:
                return <DataSetCreationDialogForm
                    dialogData={dialogData}
                    onClose={handleDialogClose}
                    open={true}
                    dataType={selectedDataType}/>;
        }
    }

    useEffect(() => {
        console.log(dialogData)
        if (dialogData.dataSetId) {
            getDataSet(dialogData.projectId, dialogData.trackId, dialogData.dataSetId).then(res => {
                let data = res as DataSet
                // @ts-ignore
                let group = GROUPS[findGroupByDataType(data.dataType)]
                setActiveGroup(group)
                setSelectedGroup(group)
                setSelectedDataType(data.dataType)
                setActiveDataType(data.dataType)
            });
        }
    }, [dialogData.dataSetId]);


    useEffect(() => {
        console.log("test")
    }, [selectedDataType, selectedGroup]);

    function handleGroupChange(event: React.ChangeEvent<{}>, group: GroupType) {
        setSelectedGroup(group)
        setActiveGroup(group)
        // @ts-ignore
        setSelectedDataType(GROUPS[group][0])
    }

    function handleElementChange(event: React.ChangeEvent<{}>, dataType: DataType) {
        setSelectedDataType(dataType)
    }

    const handleTabClick = (event: React.MouseEvent<HTMLDivElement, MouseEvent>, element: DataType) => {
        event.preventDefault();
        setSelectedDataType(element)
    };

    const displayGroupContent = () => {
        return (
            <div>
                <Tabs value={selectedDataType}
                      onChange={handleElementChange}
                      sx={{display: "flex", flexDirection: "column"}}>
                    {GROUPS[selectedGroup!].map((element) => (
                        <Tab key={element} label={element} value={element}
                             onClick={(event) => handleTabClick(event, element)}/>
                    ))}
                </Tabs>
                {renderDataContainer()}
            </div>
        )
    }

    const getGroupShowCase = () => {
        return (
            <div>
                <Tabs
                    value={selectedGroup}
                    onChange={handleGroupChange}>
                    {Object.keys(GROUPS).map((group) => (
                        <Tab key={group} label={group} value={group}/>
                    ))}
                </Tabs>
                {
                    activeGroup
                        ? displayGroupContent()
                        : null
                }
            </div>)
    }

    function findGroupByDataType(dataType: DataType): string | null {
        for (const group in GROUPS) {
            // @ts-ignore
            if (GROUPS[group].includes(dataType)) {
                return group;
            }
        }
        return null;
    }

    return (
        <Dialog
            open={open}
            onClose={onClose}
            fullWidth={false}
            maxWidth={"md"}>
            <DialogContent>
                {dialogData.dataSetId
                    ? renderDataContainer()
                    : getGroupShowCase()
                }
            </DialogContent>
        </Dialog>);
}
