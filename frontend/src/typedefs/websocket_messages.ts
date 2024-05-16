export enum WebSocketMessageType {
    SPRING = "spring",
    DJANGO = "django",
}
export interface BaseWebSocketMessage {
    message: string;
    type: WebSocketMessageType;
}

export interface MlModelTrainingProgress extends BaseWebSocketMessage{
    progress: number;
}

export interface ProjectStatusDTO extends BaseWebSocketMessage{
    status: string;
    runningTracks: TrackStatusDTO[];
}

export interface TrackStatusDTO {
    trackName: string;
    dataSetName: string;
    progress: number;
    repeating: boolean;
}


