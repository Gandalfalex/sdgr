import {useState} from 'react';
import {DataSet, DataType} from "../../../../../typedefs/spring_types";
import {deleteDataSet, editDataSet} from "../../../../../api/SpringAPI";
import i18next from "i18next";
import {DataSetProps} from "./DataSetHOC";


export function useDataSetElement(props: DataSetProps<any>) {
    const {projectId, trackId, dataSet, onEditDataSet, updateDataSet} = props;
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleUpdateCustomValues = (data: DataSet) => {
        editDataSet(data, projectId, trackId, dataSet.id).then(() => {
            updateDataSet();
        });
    };

    const handleDelete = () => {
        handleClose();
        deleteDataSet(projectId, trackId, dataSet.id).then(() => updateDataSet());
    };

    const handleEdit = () => {
        handleClose();
        onEditDataSet(dataSet.id);
    };

    return {
        anchorEl,
        handleClose,
        handleUpdateCustomValues,
        handleDelete,
        handleEdit,
    };
}


export function createData<T extends DataSet>(dataSet: T,) {

    if (dataSet.dataType === DataType.SLEEP) {
        return [{
            labelText: i18next.t("data_set_common_sleep_time", {ns: ['components']}),
            // @ts-ignore
            value: dataSet?.sleepTime as number
        }]
    }

    let data = [
        {labelText: "Data type", value: dataSet?.dataType},
        {labelText: i18next.t("data_set_common_samples", {ns: ['components']}), value: dataSet?.numSamples},
        {labelText: i18next.t("data_set_common_frequency", {ns: ['components']}), value: dataSet?.frequency},
    ];
    if (dataSet.dataType === DataType.FLOAT || dataSet.dataType === DataType.INTEGER) {
        // @ts-ignore
        data.push({labelText: i18next.t("data_set_common_season", {ns: ['components']}), value: dataSet?.season})
        // @ts-ignore
        data.push({labelText: i18next.t("data_set_common_trend", {ns: ['components']}), value: dataSet?.trend})
        // @ts-ignore
        data.push({labelText: i18next.t("data_set_common_residual", {ns: ['components']}), value: dataSet?.residual})
    }

    if (dataSet.dataType === DataType.CHAR) {
        // @ts-ignore
        data.push({labelText: i18next.t("data_set_common_alphabet", {ns: ['components']}), value: dataSet?.alphabet})
    }

    return data;
}




