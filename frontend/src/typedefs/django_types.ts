import {RJSFSchema, UiSchema} from "@rjsf/utils";

export interface TrainingData {
    id: number;
    name: string;
    size: number;
    created_at: string;
    data: Array<number>;
}

export interface TrainingDataFiles {
    id: number;
    name: string;
}

export interface Model {
    id: number;
    name: string;
    description: string;
    pyName: string;
    created_at: string;
}


export interface TrainDataPreviewDT {
    name: string;
    values: Array<number>;
}

export interface ModelConfig {
    id: number;
    name: string;
    description: string;
    processing: Preprocessor | null;
    imputation_algorithm: ImputationAlgorithm | null;
    min_length: number;
    created_at: string;
    train_data: Array<number>;
}

export interface ImputationAlgorithm {
    name: string;
    description: string;
}

export interface MlConfig extends ModelConfig {
    ml_model: number;
    is_running: string;
    solution_id: number;
}

export interface TSDConfig extends ModelConfig {
    tsd_model: number;
}

export interface TrainingInformation {
    id: number;
    ml_solution_id: number;
    added_to: string;
    training_time: number;
    iterations: number;
    accuracy: number;
    image: string;
}

export interface Preprocessor {
    id: number;
    specific_config: any;
    type: number;
    typeName: string
}

export interface PreprocessorType {
    id: number;
    name: string;
    description: string;
    schema: RJSFSchema;

}

interface Config {
    data: LevelConfig;
    levels: number;
}

export interface LevelConfig {
    [level: string]: number;
}

interface ConfigLevel {
    level: number;
    data: Array<number>;

}

export interface TSDConfigData {
    id: number;
    levels: number;
    name: string;
    level_config: Array<Config> | null;
    values: Array<ConfigLevel>;
    type: string;
}

export interface InputForms {
    schema: RJSFSchema;
    ui_schema: UiSchema;
}

export interface TrainDataPreviewComplete {
    original: TrainDataPreviewDT;
    preview: TrainDataPreviewDT;
    flags: Array<boolean>;
}

export interface TrainDataInformation {
    "id": number;
    "contains_gaps": string;
    "name": string;
    "created_at": string;
    "size": number;
    "range": any;
    "ml_count": number;
    "tsd_count": number;
}

export interface OffsetsMapping {
    [step: number]: OffsetDetails;
}

export interface OffsetDetails {
    value?: number;
    allow?: boolean;
}