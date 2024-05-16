import {createData, useDataSetElement} from "./DataSetHook";
import {SleepDataSet} from "../../../../../typedefs/spring_types";
import {CardSkeleton} from "../skeletons/CardSkeleton";
import OverviewTableContainer from "../skeletons/OverviewTableContainer";
import React from "react";
import {SleepDataSetProps} from "./DataSetHOC";

export const SleepDataSetElement = (props: SleepDataSetProps) => {
    const {dataSet} = props;
    const {handleDelete, handleEdit} = useDataSetElement(props);
    let data = createData<SleepDataSet>(dataSet)

    return (
        <CardSkeleton title={dataSet?.name}
                      dataType={dataSet.dataType}
                      onEdit={handleEdit}
                      onDelete={handleDelete}
                      totalSteps={1}>
            <OverviewTableContainer data={data}/>
            <></>
        </CardSkeleton>

    );
}