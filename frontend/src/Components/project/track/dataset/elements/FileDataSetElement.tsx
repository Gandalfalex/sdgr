import {createData, useDataSetElement} from "./DataSetHook";
import {FileDataSet, PreviewData} from "../../../../../typedefs/spring_types";
import {CardSkeleton} from "../skeletons/CardSkeleton";
import OverviewTableContainer from "../skeletons/OverviewTableContainer";
import React, {useEffect, useState} from "react";
import PreviewDataContainer from "../skeletons/PreviewDataContainer";
import {SingleValues} from "../SingleValues";
import {getDataSetPreview} from "../../../../../api/SpringAPI";
import {FileDataSetProps} from "./DataSetHOC";

export const FileDataSetElement = (props: FileDataSetProps) => {
    const {projectId, trackId, dataSet} = props;
    const {handleUpdateCustomValues, handleDelete, handleEdit} = useDataSetElement(props);

    const [previewData, setPreviewData] = useState<PreviewData>();

    let data = createData<FileDataSet>(dataSet)

    // update preview when dataset changes
    useEffect(() => {
        getDataSetPreview(projectId, trackId, dataSet.id).then(res => setPreviewData(res));
    }, [dataSet]) // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        getDataSetPreview(projectId, trackId, dataSet.id).then(res => setPreviewData(res));
    }, [])  // eslint-disable-line react-hooks/exhaustive-deps


    return (
        <CardSkeleton title={dataSet?.name}
                      dataType={dataSet.dataType}
                      onEdit={handleEdit}
                      onDelete={handleDelete}
                      totalSteps={3}>
            <OverviewTableContainer data={data}/>
            <PreviewDataContainer previewData={previewData}/>
            <SingleValues dataSet={dataSet} updateDataSet={handleUpdateCustomValues}/>
        </CardSkeleton>
    );
}