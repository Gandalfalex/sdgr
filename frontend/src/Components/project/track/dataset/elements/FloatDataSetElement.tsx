import React, {useEffect, useState} from "react";
import {getDataSetPreview} from "../../../../../api/SpringAPI";
import {FloatDataSet, PreviewData} from "../../../../../typedefs/spring_types";
import {SingleValues} from "../SingleValues";
import {CardSkeleton} from "../skeletons/CardSkeleton";
import OverviewTableContainer from "../skeletons/OverviewTableContainer";
import PreviewDataContainer from "../skeletons/PreviewDataContainer";
import {createData, useDataSetElement} from "./DataSetHook";
import {FloatDataSetProps} from "./DataSetHOC";


export const FloatDataSetElement = (props: FloatDataSetProps) => {
    const {projectId, trackId, dataSet} = props;
    const {handleUpdateCustomValues, handleDelete, handleEdit} = useDataSetElement(props);

    const [previewData, setPreviewData] = useState<PreviewData>();

    let data = createData<FloatDataSet>(dataSet)

    // update preview when dataset changes
    useEffect(() => {
        getDataSetPreview(projectId, trackId, dataSet.id).then(res => setPreviewData(res));
    }, [dataSet]) // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        getDataSetPreview(projectId, trackId, dataSet.id).then(res => setPreviewData(res));
    }, [])  // eslint-disable-line react-hooks/exhaustive-deps
    return (
        <CardSkeleton title={dataSet?.name}
                      onEdit={handleEdit}
                      dataType={dataSet.dataType}
                      onDelete={handleDelete}
                      totalSteps={3}>
            <OverviewTableContainer data={data}/>
            <PreviewDataContainer previewData={previewData}/>
            <SingleValues dataSet={dataSet} updateDataSet={handleUpdateCustomValues}/>
        </CardSkeleton>
    );
}
