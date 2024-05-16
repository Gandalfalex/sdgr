import React from "react";
import {SingleValues} from "../SingleValues";
import {CardSkeleton} from "../skeletons/CardSkeleton";
import OverviewTableContainer from "../skeletons/OverviewTableContainer";
import { createData, useDataSetElement} from "./DataSetHook";
import {CharDataSet} from "../../../../../typedefs/spring_types";
import {CharDataSetProps} from "./DataSetHOC";


export const CharDataSetElement = (props: CharDataSetProps) => {
    const {dataSet} = props;
    const {handleUpdateCustomValues, handleDelete, handleEdit } = useDataSetElement(props);
    let data = createData<CharDataSet>(dataSet)

    return (
        <CardSkeleton title={dataSet?.name} dataType={dataSet.dataType} onEdit={handleEdit} onDelete={handleDelete} totalSteps={2}>
            <OverviewTableContainer data={data}/>
            <SingleValues dataSet={dataSet} updateDataSet={handleUpdateCustomValues}/>
        </CardSkeleton>

    );
}
