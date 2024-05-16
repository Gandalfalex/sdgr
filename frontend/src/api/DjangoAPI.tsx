import {djangoAPI, WS_DJANGO_URL} from "./ApiConnector";
import SnackbarComponent from "../Components/shared_components/snackbar/SnackBarComponent";
import {SnackbarSeverity} from "../typedefs/error_types";


const WS_URL = WS_DJANGO_URL

const token = sessionStorage.getItem('jwt');


let api = djangoAPI;

const handleError = (error: any) => {
    throw error;
};

export function getMlModels() {
    return api.get(`/ml/ml_model`).then(res => res.data);
}

export function getMlModelById(id: number) {
    return api.get(`/ml/ml_model/${id}`).then(res => res.data).catch(handleError);
}

export function getAllSolutionsByModelId(mId: number) {
    return api.get(`/ml/ml_model/${mId}/ml_solution/`).then(res => res.data).catch(handleError);
}

export function getMlConfigByModelIdAndConfigId(mId: number, id: number) {
    return api.get(`/ml/ml_model/${mId}/ml_solution/${id}`).then(res => res.data).catch(handleError);
}

export function deleteSolutionByID(mId: number, id: number) {
    return api.delete(`/ml/ml_model/${mId}/ml_solution/${id}`).then(res => res.data).catch(handleError);
}

export function getTrainingData(id: number) {
    return api.get(`/training_data`).then(res => res.data).catch(handleError);
}

export function getSpecificTrainingData(id: number) {
    return api.get(`/training_data/${id}`).then(res => res.data).catch(handleError);
}

export function deleteSpecificTrainingData(id: number) {
    return api.delete(`/training_data/${id}`).then(res => res.data).catch(handleError);
}

export function getSpecificTrainingDataIformation(id: number) {
    return api.get(`/training_data/${id}/information`).then(res => res.data).catch(handleError);
}

export function getAllTrainingData(complete: string) {
    return api.get(`/training_data/?get_complete_data=${complete}`).then(res => res.data).catch(handleError);
}

export function getUserFiles() {
    return api.get(`/training_data/files`).then(res => res.data).catch(handleError);
}

export function getTrainingDataForFiles(id: number) {
    return api.get(`/training_data/files/${id}`).then(res => res.data).catch(handleError);
}

export function deleteTrainingDataForFiles(id: number) {
    return api.delete(`/training_data/files/${id}`).then(res => res.data).catch(handleError);
}

export function getAllTrainingDataForSolutionReduced(mId: number, id: number) {
    return api.get(`/ml/ml_model/${mId}/ml_solution/${id}/reduced_data`).then(res => res.data).catch(handleError);
}

export function uploadTrainingFiles(files: Array<File>) {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });
    return api.post(`/training_data/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(res => res.data).catch(handleError);
}


export function postNewSolutionSet(mlId: number, name: string, description: string, trainingData: Array<number>, trainingDataFiles: Array<number>) {
    const data = {
        "name": name,
        "description": description,
        "train_data": trainingData,
        "files": trainingDataFiles
    };
    return api.post(`/ml/ml_model/${mlId}/ml_solution/`, data).then(res => res.data).catch(handleError);
}

export function patchSolutionSet(mlId: number, id: number, name: string, description: string, trainingData: Array<number>, trainingDataFiles: Array<number>) {
    const data = {
        "name": name,
        "description": description,
        "train_data": trainingData,
        "files": trainingDataFiles
    };
    return api.patch(`/ml/ml_model/${mlId}/ml_solution/${id}`, data).then(res => res.data).catch(handleError);
}

export function copySolutionSet(mlId: number, id: number) {
    return api.post(`/ml/ml_model/${mlId}/ml_solution/${id}/copy`).then(res => res.data).catch(handleError);
}

export function getInformationAboutConfiguration(mId: number, id: number) {
    return api.get(`/ml/ml_model/${mId}/config/${id}`).then(res => res.data).catch(handleError);
}


export function createTrainingWebSocket(modelId: number, id: number) {
    return `${WS_URL}/ws/status/?token=${token}&ml_id=${modelId}&sol_id=${id}`
}


export function getProcessingSchema() {
    return api.get("/preprocessor/").then(res => res.data).catch(handleError)
}

export function postPreprocessorConfigML(mlId: number, id: number, json: any) {
    return api.post(`/ml/ml_model/${mlId}/ml_solution/${id}/preprocessor`, json).then(res => res.data).catch(handleError);
}


export function getTsdModels() {
    return api.get(`/tsd/tsd_model/`).then(res => res.data).catch(handleError);
}

export function getTsdModel(id: number) {
    return api.get(`/tsd/tsd_model/${id}`).then(res => res.data).catch(handleError);
}


export function getTSDConfigByModelId(tsd: number) {
    return api.get(`/tsd/tsd_model/${tsd}/tsd_configuration/`).then(res => res.data).catch(handleError);
}

export function getTsdConfigurationById(tsd: number, id: number) {
    return api.get(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}`).then(res => res.data).catch(handleError);
}

export function getTsdConfigurationData(tsd: number, id: number) {
    return api.get(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}/configure`).then(res => res.data).catch(handleError);
}

export function getTsdConfigurationDataForSingleDataSet(tsd: number, id: number, td: number) {
    return api.get(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}/configure/${td}`).then(res => res.data).catch(handleError);
}

export function postTSDConfiguration(tsd: number, name: string, description: string, trainingData: Array<number>, files: Array<number>) {
    const data = {
        "name": name,
        "description": description,
        "train_data": trainingData,
        "files": files
    };
    return api.post(`/tsd/tsd_model/${tsd}/tsd_configuration/`, data).then(res => res.data).catch(handleError);
}

export function patchTSDConfiguration(tsd: number, id: number, name: string, description: string, trainingData: Array<number>, files: Array<number>) {
    const data = {
        "name": name,
        "description": description,
        "train_data": trainingData,
        "files":files
    };
    return api.patch(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}`, data).then(res => res.data).catch(handleError);
}

export function deleteTsdConfigurationById(tsd: number, id: number) {
    return api.delete(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}`).then(res => res.data).catch(handleError);
}

export function getAllTrainingDataForConfigReduced(tsd: number, id: number) {
    return api.get(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}/reduced_data/`).then(res => res.data).catch(handleError);
}


export function postPreprocessorConfigTSD(tsd: number, id: number, json: any) {
    return api.post(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}/preprocessor`, json).then(res => res.data).catch(handleError);
}

export function uploadForPreview(files: Array<File>, json: any, id?: number, fileId?: number) {
    const formData = new FormData();
    files.forEach(file => {
        formData.append('files', file);
    });
    formData.append("metadata", JSON.stringify(json));
    if (id || fileId) {
        formData.append("train_data", JSON.stringify({train_data: id, file: fileId}))
    }
    return api.post(`preprocessor/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    }).then(res => res.data).catch(handleError);
}

export function postConfigForTsd(tsd: number, id: number, tdId: number, json: any) {
    return api.post(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}/add_levels/${tdId}`, json).then(res => res.data).catch(handleError);
}

export function postCopyConfig(tsd: number, id: number) {
    return api.post(`/tsd/tsd_model/${tsd}/tsd_configuration/${id}/copy`).then(res => res.data).catch(handleError);
}

export function postSurvey(data: any) {
    return api.post('/survey', data).then(res => res.data).catch(handleError);
}