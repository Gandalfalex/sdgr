export interface SaveData {
    validInput: boolean;
    validConfiguration: boolean;
    message: string;
}

export enum SnackbarSeverity {
    ERROR = "error",
    INFO = "info",
    SUCCESS = "success",
    WARNING = "warning",
}


export type RSJFError = {
    name?: string;
    property?: string;
    message?: string;
    params?: Record<string, any>;
};