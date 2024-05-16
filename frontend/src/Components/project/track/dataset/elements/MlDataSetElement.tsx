import React, {useEffect, useState} from "react";
import {SingleValues} from "../SingleValues";
import {CardSkeleton} from "../skeletons/CardSkeleton";
import {createData, useDataSetElement} from "./DataSetHook";
import {MLConfig, MLDataSet, MlModel} from "../../../../../typedefs/spring_types";
import ComplexOverviewTableContainer from "../skeletons/ComplexOverviewTableContainer";
import {getMlConfigByModelIdAndConfigId, getMlModelById} from "../../../../../api/DjangoAPI";
import {MlDataSetProps} from "./DataSetHOC";


export const MlDataSetElement = (props: MlDataSetProps) => {
    const { dataSet} = props;
    const { handleUpdateCustomValues, handleDelete, handleEdit } = useDataSetElement(props);
    let data = createData<MLDataSet>(dataSet)
    const [model, setModel] = useState<MlModel | null>(null)
    const [config, setConfig] = useState<MLConfig | null>(null)

    useEffect(() => {
        getMlModelById(props.dataSet.modelId).then(setModel);
        getMlConfigByModelIdAndConfigId(props.dataSet.modelId, props.dataSet.configurationId).then(setConfig);
    }, []);
    return (
        <CardSkeleton title={dataSet?.name} dataType={dataSet.dataType} onEdit={handleEdit} onDelete={handleDelete} totalSteps={2}>
            <ComplexOverviewTableContainer data={data} configuration={config?.name} model={model?.name} trainingDataSize={1}/>
            <SingleValues dataSet={dataSet} updateDataSet={handleUpdateCustomValues}/>
        </CardSkeleton>
    );
}
