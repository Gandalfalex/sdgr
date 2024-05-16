import {JsonSchema7} from "@jsonforms/core";

export type Projects = Array<Project>

export interface Project {
    id: number;
    name: string;
    sending: boolean;
}

export type Tracks = Array<Track>

export interface Track {
    id: number,
    repeating: boolean,
    name: string,
    unit: string,
    allowedDataTypes: Array<DataTypeSchema>
}

export type CustomValue = {
    sampleNum: number,
    value: number
}

export type Trend = {
    type: string,
    displayName: string
}

export type Season = {
    type: string,
    displayName: string
}

export type Residual = {
    type: string,
    displayName: string
}

export type DataSetDialogData = {
    dataSetId: number | null,
    projectId: number,
    trackId: number,
}

export interface DataSetSelected {
    selectedTrend: Trend | undefined,
    selectedSeason: Season | undefined,
    selectedResidual: Residual | undefined,
}

export interface PreviewData {
    labels: Array<number>,
    values: Array<number>
}

export type LogMessages = Array<LogMessage>

export interface LogMessage {
    message: string,
    time: string,
    sendSession: string,
    dataSetName: string,
}

export interface LogDataGraph {
    labels: Array<number>,
    values: Array<number>
}

export interface LogSession {
    session: string,
}

export enum CalculationMethod {
    ADDITIVE = "additive",
    MULTIPLICATIVE = "multiplicative"
}

type DataSetType = "float" | "integer" | "char" | "ml" | "tsa" | "sleep" | "filetype";
export type DataSet = {
    id: number,
    name: string,
    frequency: number,
    numSamples: number,
    position: number,
    type: DataSetType,
    dataType: DataType,
    customValues: Array<CustomValue>,
}

export interface FloatDataSet extends DataSet {
    type: "float",
    dataType: DataType.FLOAT,
    calculationMethod: CalculationMethod,
    seed: number,
    trendOption: Trend;
    seasonOption: Season;
    residualOption: Residual;
    trend: string,
    season: string,
    residual: string
}

export interface IntegerDataSet extends DataSet {
    type: "integer",
    dataType: DataType.INTEGER,
    calculationMethod: CalculationMethod,
    seed: number,
    trend: Trend,
    season: Season,
    residual: Residual
}

export interface CharDataSet extends DataSet {
    type: "char",
    alphabet: string,
    dataType: DataType.CHAR,
}

export interface MLDataSet extends DataSet {
    type: "ml";
    modelId: number;
    configurationId: number;
    dataType: DataType.ML;
}

export interface TSADataSet extends DataSet {
    type: "tsa";
    configurationId: number;
    modelId: number;
    dataType: DataType.TSA;
    configs: Array<Config>;
}

export interface SleepDataSet extends DataSet {
    type: "sleep";
    sleepTime: number;
    dataType: DataType.SLEEP;
}

export interface FileDataSet extends DataSet {
    type: "filetype";
    trainDataId: number;
    dataType: DataType.FILETYPE;
}


export interface Config {
    trainDataId: number;
    level_configs: {
        [key: string]: number;
    };
}

export interface FloatDataSetFormState {
    trendStrategies: Array<Trend>,
    seasonStrategies: Array<Season>,
    residualStrategies: Array<Residual>,
    ready: boolean,
    formData: any
}

export enum DataType {
    FLOAT = "FLOAT",
    CHAR = "CHAR",
    INTEGER = "INTEGER",
    NONE = "NONE",
    ML = "ML",
    TSA = "TSA",
    SLEEP = "SLEEP",
    FILETYPE = "FILETYPE"
}

export interface DataTypeSchema {
    name: DataType;
    description: String;
    data_type: DataType;
    in_preview_visible: boolean;
    schema: JsonSchema7;
}

export interface DataSetFormState {
    ready: boolean,
    formData: any
}


export interface MlModel {
    "id": number,
    "name": string,
    "description": string,
    "created_at": string
}

export interface MLConfig {
    "id": number,
    "name": string,
    "mlmodel_id": number,
    "created_at": string,
    "training_time": number,
    "training_iterations": number,
    "accuracy": number,
    "max_length": number,
}

export interface ModelOccurrence {
    projectId: number;
    trackId: number;
    dataSetId: number;
    projectName: string;
    trackName: string;
    dataSetName: string;
}

export interface TrainDataDTO {
    id: number;
    name: string;
}

interface TrackStatusDTO {
    id: number;
    trackName: string;
    dataSetName: string;
    progress: number;
}

interface ProjectStatusDTO {
    type: string;
    id: number;
    status: 'running' | 'stopped';
    runningTracks: TrackStatusDTO[];
    startTime: string;
    message: string | null;
}

export type GroupType = keyof typeof GROUPS;
export const GROUPS = {
    PRIMITIVE_DATA: [DataType.FLOAT, DataType.INTEGER, DataType.CHAR],
    GENERATED_DATA: [DataType.ML, DataType.TSA, DataType.FILETYPE],
    TIMING: [DataType.SLEEP],
};

export interface KafkaConfig {
    bootstrapServerAddress: string;
    groupId: string;
    topic: string;
    topicId: number;
}

export interface User {
    name: string;
    mail: string;
}