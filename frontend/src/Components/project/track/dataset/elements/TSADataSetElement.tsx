import React, {useEffect, useState} from "react";
import {SingleValues} from "../SingleValues";
import {CardSkeleton} from "../skeletons/CardSkeleton";
import {createData, useDataSetElement} from "./DataSetHook";
import {TSADataSet} from "../../../../../typedefs/spring_types";
import ComplexOverviewTableContainer from "../skeletons/ComplexOverviewTableContainer";
import {getTsdConfigurationById, getTsdModel} from "../../../../../api/DjangoAPI";
import {Model, TSDConfig} from "../../../../../typedefs/django_types";
import {TSADataSetProps} from "./DataSetHOC";

export const TSDDataSetElement = (props: TSADataSetProps) => {
    const { dataSet} = props;
    const { handleUpdateCustomValues, handleDelete, handleEdit } = useDataSetElement(props);
    let data = createData<TSADataSet>(dataSet)
    const [model, setModel] = useState<Model | null>(null)
    const [config, setConfig] = useState<TSDConfig | null>(null)

    useEffect(() => {
        getTsdModel(props.dataSet.modelId).then(setModel);
        getTsdConfigurationById(props.dataSet.modelId, props.dataSet.configurationId).then(setConfig);
    }, []);
    return (
        <CardSkeleton title={dataSet?.name} dataType={dataSet.dataType} onEdit={handleEdit} onDelete={handleDelete} totalSteps={2}>
            <ComplexOverviewTableContainer data={data} configuration={config?.name} model={model?.name} trainingDataSize={dataSet.configs.length}/>
            <SingleValues dataSet={dataSet} updateDataSet={handleUpdateCustomValues}/>
        </CardSkeleton>
    );
}
