import {
    CharDataSet,
    DataSet,
    DataType, FileDataSet,
    FloatDataSet,
    IntegerDataSet,
    MLDataSet, SleepDataSet,
    TSADataSet
} from "../../../../../typedefs/spring_types";
import {SleepDataSetElement} from "./SleepDataSetElement";
import {TSDDataSetElement} from "./TSADataSetElement";
import {CharDataSetElement} from "./CharDataSetElement";
import {FloatDataSetElement} from "./FloatDataSetElement";
import {IntegerDataSetElement} from "./IntegerDataSetElement";
import {MlDataSetElement} from "./MlDataSetElement";
import {FileDataSetElement} from "./FileDataSetElement";

type DataSetComponentProps = {
    dataSet: DataSet;
    projectId: number;
    trackId: number;
    updateDataSet: () => void;
    onEditDataSet: (dataSetId: number) => void;
};

export function getDataType<T>(type: DataType, element: T) {
    switch (type) {
        case DataType.FLOAT:
            return element as FloatDataSet
        case DataType.SLEEP:
            return element as SleepDataSet
        case DataType.INTEGER:
            return element as IntegerDataSet
        case DataType.ML:
            return element as MLDataSet
        case DataType.CHAR:
            return element as CharDataSet
        case DataType.TSA:
            return element as TSADataSet
        case DataType.FILETYPE:
            return element as FileDataSet
        case DataType.NONE:
            return element
    }
}



const withDataSet = (Component: React.ComponentType<any>) => {
    return (props: DataSetComponentProps) => {
        const { dataSet, ...rest } = props;
        const castedDataSet = getDataType(dataSet.dataType, dataSet);
        return <Component dataSet={castedDataSet} {...rest} />;
    };
};

export const DataSetTypeMap = {
    [DataType.FLOAT]: withDataSet(FloatDataSetElement),
    [DataType.CHAR]: withDataSet(CharDataSetElement),
    [DataType.INTEGER]: withDataSet(IntegerDataSetElement),
    [DataType.ML]: withDataSet(MlDataSetElement),
    [DataType.TSA]: withDataSet(TSDDataSetElement),
    [DataType.SLEEP]: withDataSet(SleepDataSetElement),
    [DataType.FILETYPE]: withDataSet(FileDataSetElement),
    [DataType.NONE]: withDataSet(SleepDataSetElement),
};


export interface DataSetProps<T> {
    projectId: number;
    trackId: number;
    dataSet: T;
    onEditDataSet: (dataSetId: number) => void;
    updateDataSet: () => void;
}

export type FloatDataSetProps = DataSetProps<FloatDataSet>;
export type CharDataSetProps = DataSetProps<CharDataSet>;
export type MlDataSetProps = DataSetProps<MLDataSet>;
export type TSADataSetProps = DataSetProps<TSADataSet>;
export type IntegerDataSetProps = DataSetProps<IntegerDataSet>;
export type SleepDataSetProps = DataSetProps<SleepDataSet>;
export type FileDataSetProps = DataSetProps<FileDataSet>;