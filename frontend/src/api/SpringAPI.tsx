import {Project, Projects, Track} from "../typedefs/spring_types";
import {springAPI, WS_SPRING_URL} from "./ApiConnector";

const BASE_URL = WS_SPRING_URL


const token = sessionStorage.getItem('jwt');
let api = springAPI;

const handleError = (error: any) => {
    console.error("API call failed:", error);
    throw error; // Re-throw the error to let the calling code handle it further if needed
};


export function deleteProject(id: number) {
    return api.delete(`/api/projects/${id}`).then(res => res.data).catch(handleError);
}

export function getProject(id: string) {
    return api.get(`/api/projects/${id}`).then(res => res.data).catch(handleError);
}

export function putProject(project: Project) {
    const data = {
        "id": project.id,
        "name": project.name,
        "sending": project.sending
    };
    return api.put(`/api/projects/${project.id}`, data).then(res => res.data).catch(handleError);
}

export function getUser() {
    return api.get('/api/user').then(res => res.data).catch(handleError);
}

export function getAllProjects(): Promise<Projects> {
    return api.get(`/api/projects`).then(res => res.data).catch(handleError);
}

export function putNewProject(name: String) {
    const data = {
        "name": name,
    };
    return api.post(`/api/projects`, data).then(res => res.data).catch(handleError);
}

export function getAllTracks(projectId: string) {
    return api.get(`/api/projects/${projectId}/tracks`).then(res => res.data).catch(handleError);
}

export function createTrack(projectId: string, newTrack: Track) {
    return api.post(`/api/projects/${projectId}/tracks`, newTrack).then(res => res.data).catch(handleError);
}

export function editTrack(projectId: number, trackId: number, data: Track) {
    return api.put(`/api/projects/${projectId}/tracks/${trackId}`, data).then(res => res.data).catch(handleError);
}

export function deleteTrack(projectId: number, trackId: number) {
    return api.delete(`/api/projects/${projectId}/tracks/${trackId}`).then(res => res.data).catch(handleError);
}

export function getSchema(category: string, selection: string): Promise<any> {
    return api.get(`/api/strategies/${category}/${selection}`).then(res => res.data).catch(handleError);
}

export function createDataSet(data: any, projectId: number, trackId: number): Promise<any> {
    return api.post(`/api/projects/${projectId}/tracks/${trackId}/datasets`, data).then(res => res.data).catch(handleError);
}

export function editDataSet(data: any, projectId: number, trackId: number, dataSetId: number): Promise<any> {
    console.log(data)
    return api.put(`/api/projects/${projectId}/tracks/${trackId}/datasets/${dataSetId}`, data).then(res => res.data).catch(handleError);
}

export function getAllDataSets(projectId: number, trackId: number) {
    return api.get(`/api/projects/${projectId}/tracks/${trackId}/datasets`).then(res => res.data).catch(handleError);
}

export function getDataSet(projectId: number, trackId: number, dataSetId: number) {
    return api.get(`/api/projects/${projectId}/tracks/${trackId}/datasets/${dataSetId}`).then(res => res.data).catch(handleError);
}


export function deleteDataSet(projectId: number, trackId: number, dataSetId: number) {
    return api.delete(`/api/projects/${projectId}/tracks/${trackId}/datasets/${dataSetId}`).then(res => res.data).catch(handleError);
}

export function getDataSetPreview(projectId: number, trackId: number, dataSetId: number) {
    return api.get(`/api/projects/${projectId}/tracks/${trackId}/datasets/${dataSetId}/preview`).then(res => res.data).catch(handleError);
}

export function getTrackLogs(trackId: number, page_size: number, page_number: number, search_query: string) {
    return api.get(`/api/logs/${trackId}?page_size=${page_size}&page_number=${page_number}&search_query=${search_query}`).then(res => res.data).catch(handleError);
}

export function getLogSize(trackId: number, search_query: string) {
    return api.get(`/api/logs/${trackId}/log_size?search_query=${search_query}`).then(res => res.data).catch(handleError);
}

export function getLogSessions(trackId: number) {
    return api.get(`/api/logs/${trackId}/logSessions`).then(res => res.data).catch(handleError);
}

export function getLogSessionGraph(trackId: number, session: string) {
    return api.get(`/api/logs/${trackId}/logGraph?session=${session}`).then(res => res.data).catch(handleError);
}


export function getDataTypes() {
    return api.get(`/api/data_types/dataTypes`).then(res => res.data).catch(handleError);
}

export function postDataType() {
    return api.get(`/api/data_types/dataTypes`).then(res => res.data).catch(handleError);
}

export function getDataTypeByName(name: string, params = {}) {
    return api.get(`/api/data_types/dataTypes/${name}`, {params}).then(res => res.data).catch(handleError);
}

export function getFloatSchema() {
    return api.get(`/api/strategies/numeric`).then(res => res.data).catch(handleError);
}

export function getMlModels() {
    return api.get(`/api/django/ml`).then(res => res.data).catch(handleError);
}

export function getMlModelsWithConfiguration() {
    return api.get(`/api/django/ml/configured`).then(res => res.data).catch(handleError);
}

export function getMlConfigurationsByModelId(id: number) {
    return api.get(`/api/django/ml/${id}`).then(res => res.data).catch(handleError);
}

export function getMlConfigurationByModelIdAndConfigId(id: number, configId: number) {
    return api.get(`/api/django/ml/${id}/config/${configId}`).then(res => res.data).catch(handleError);
}


export function findAllOccurancesOfMLConfiguration(id: number) {
    return api.get(`/api/projects/ml/datasets/${id}`).then(res => res.data).catch(handleError);
}


export function getTSDModels() {
    return api.get(`/api/django/tsd`).then(res => res.data).catch(handleError);
}

export function getTSDModelsWithConfiguration() {
    return api.get(`/api/django/tsd/configured`).then(res => res.data).catch(handleError);
}

export function getTSDConfigurationByModelId(id: number) {
    return api.get(`/api/django/tsd/${id}`).then(res => res.data).catch(handleError);
}

export function findAllOccurancesOfTSDConfiguration(id: number) {
    return api.get(`/api/projects/tsd/datasets/${id}`).then(res => res.data).catch(handleError);
}

export function findAllTrainDataOfConfiguration(modelId: number, configId: number) {
    return api.get(`/api/django/tsd/${modelId}/tsd_config/${configId}/trainData`).then(res => res.data).catch(handleError);
}

export function createStartSendingWebSocket(id: string) {
    return `${BASE_URL}/start-project?token=${token}&id=${id}`
}

export function getConfigurationForKafka(modelId: number) {
    return api.get(`/api/kafka/${modelId}`).then(res => res.data).catch(handleError);
}