import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import {Box, Card, CardHeader, Grid, IconButton, Tooltip, Typography} from "@mui/material";
import React, {useEffect, useState} from "react";
import {useLocation, useNavigate, useParams} from "react-router-dom";
import {Project, Track, Tracks} from "../../typedefs/spring_types";
import {createStartSendingWebSocket, createTrack, getAllTracks, getProject,} from "../../api/SpringAPI";
import {TrackDialog} from "../dialogs/TrackDialog";
import {TrackElement} from "./track/TrackElement";
import CloseIcon from '@mui/icons-material/Close';
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../../typedefs/error_types";
import {useWebSocket} from "../websockets/WebSocketProvider";
import WebSocketMessagesDrawerComponent from "../websockets/WebSocketDrawerComponent";
import {ProjectStatusDTO} from "../../typedefs/websocket_messages";
import {PaperContainerComponent} from "../shared_components/paper/PaperComponent";
import {ElementCardComponent} from "../shared_components/cards/ElementCardComponent";
import GenericAccordion from "../shared_components/GenericAccordion";
import {ProjectStartDialog} from "../dialogs/ProjectStartDialog";
import {NewElementButton} from "../buttons/NewElementButton";
import {useTranslation} from "react-i18next";

export const ProjectOverview = () => {
    const {projectId} = useParams();
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const expandIDFromURL = queryParams.get('expandID');
    const [expandID, setExpandId] = useState<number | null>(expandIDFromURL ? parseInt(expandIDFromURL) : null);

    const [project, updateProject] = useState<Project>();
    const [tracks, setAllTracks] = useState<Tracks>([]);
    const navigate = useNavigate();
    const [showNewTrackDialog, setShowNewTrackDialog] = useState(false);
    const {showMessage} = useSnackbar();
    const {connect, disconnect, sendMessage} = useWebSocket();
    const [openKafkaDialog, setOpenKafkaDialog] = useState(false)
    const {t} = useTranslation(['dialogs']);

    const handleExpandClick = (id: number | null) => {
        setExpandId((lastID) => {
            return (lastID === id) ? null : id;
        });
    }

    const handleBack = () => {
        navigate(`/`);
    }

    const handleStartSending = () => {
        connect(createStartSendingWebSocket(projectId!),
            {
                onMessage: handleWebsocketMessage,
                onClose: handleClose,
                onError: handleError
            }, true, projectId!);
        updateProject((oldState) => ((oldState) ? {
            ...oldState,
            sending: true
        } : oldState));
        setOpenKafkaDialog(false)
    };

    const openKafkaConfigDialog = () => {
        setOpenKafkaDialog(true)
    }
    const handleWebsocketMessage = (data: string) => {
        try {
            const dataObject = JSON.parse(data) as ProjectStatusDTO;
            showMessage(dataObject.message, SnackbarSeverity.INFO)
        } catch (error) {
            console.error("Error parsing JSON:", error);
        }
    };

    const handleClose = () => {
        showMessage("stop running", SnackbarSeverity.INFO);
    };

    const handleError = (event: Event) => {
        showMessage("something went wrong:" + event, SnackbarSeverity.ERROR);
    };


    //TODO change this!
    const handleStopSending = () => {
        if (projectId) {
            sendMessage(createStartSendingWebSocket(projectId), projectId!, projectId);
            updateProject((oldState) => ((oldState) ? {
                ...oldState,
                sending: false
            } : oldState));
            showMessage("stop sending", SnackbarSeverity.INFO)
        }
        disconnect(createStartSendingWebSocket(projectId!))
    }

    const openNewTrackDialog = (open: boolean) => {
        setShowNewTrackDialog(open);
    }

    const handleCloseNewTrackDialog = (newTrack?: Track) => {
        setShowNewTrackDialog(false);

        if (projectId && newTrack) {
            createTrack(projectId, newTrack)
                .then(res => {
                    getAllTracks(projectId)
                        .then(res => {
                            setAllTracks(res);
                        })
                        .catch(err => {
                            showMessage(err, SnackbarSeverity.WARNING)
                        });
                })
                .catch(err => {
                    showMessage(err, SnackbarSeverity.WARNING)
                });
        }
    }

    const refreshTracks = () => {
        if (projectId) {
            getAllTracks(projectId)
                .then(res => {
                    setAllTracks(res);
                })
                .catch(err => {
                    showMessage(err, SnackbarSeverity.WARNING)
                });
        }
    }

    useEffect(() => {
        if (projectId) {
            getProject(projectId).then(res => updateProject(res)).then(x => {
                if (project && project.sending) {
                    handleStartSending();
                }
            });
            getAllTracks(projectId).then(res => setAllTracks(res));
        }
    }, [])  // eslint-disable-line react-hooks/exhaustive-deps
    if (!projectId) {
        return (<div/>);
    }
    return (
        <PaperContainerComponent>
            <Card style={{border: "none", boxShadow: "none"}}>
                <CardHeader sx={{pl: 5, pt: 4}} title={
                    <Box sx={{display: "flex", alignItems: 'center'}}>
                        <Typography variant={"h5"}>{project?.name}</Typography>
                        {project?.sending ?
                            <Tooltip title="Stop sending" arrow>
                                <IconButton className={'growButton'}
                                            onClick={handleStopSending}><StopIcon/></IconButton>
                            </Tooltip>
                            :
                            <Tooltip title="Start sending" arrow>
                                <IconButton className={'growButton'}
                                            onClick={openKafkaConfigDialog}><PlayArrowIcon/></IconButton>
                            </Tooltip>
                        }

                    </Box>
                } avatar={
                    project?.sending ?
                        <Tooltip title={t('project_sending', {ns: ['dialogs']})}>
                            <div className={"circle"}></div>
                        </Tooltip> :
                        <Tooltip title={t('project_not_sending', {ns: ['dialogs']})}>
                            <div className={"circleOffline"}></div>
                        </Tooltip>
                }
                            action={
                                <div>
                                    <Tooltip title="Close project" arrow>
                                        <IconButton className={'growButton'}
                                                    onClick={handleBack}>
                                            <CloseIcon/>
                                        </IconButton>
                                    </Tooltip>
                                </div>
                            }>
                </CardHeader>
            </Card>
            <ElementCardComponent>
                {tracks.length !== 0 ?
                    tracks.map((track) => (
                        <Grid key={track.id} item xs={1}>
                            <GenericAccordion
                                expanded={track.id === expandID}
                                onChange={() => setExpandId(expandID === track.id ? null : track.id)}
                                details={
                                    <TrackElement
                                        projectId={parseInt(projectId)} track={track}
                                        expanded={track.id === expandID}
                                        handleExpandClick={handleExpandClick}
                                        refreshTracks={refreshTracks}/>}
                                header={track.name + " [" + track.unit + "]"}
                            />
                        </Grid>
                    ))
                    : null}
                <NewElementButton
                    message={t('new_track', {ns: ['dialogs']})}
                    handleClick={openNewTrackDialog}/>
                <TrackDialog
                    id="new-track"
                    isEdit={false}
                    keepMounted
                    open={showNewTrackDialog}
                    onClose={handleCloseNewTrackDialog} value={{
                    id: 0,
                    name: "",
                    repeating: false,
                    unit: "",
                    allowedDataTypes: []
                }}/>
                <ProjectStartDialog
                    onClose={() => setOpenKafkaDialog(false)}
                    open={openKafkaDialog}
                    projectId={parseInt(projectId)}
                    startSending={handleStartSending}/>
            </ElementCardComponent>
            <WebSocketMessagesDrawerComponent/>
        </PaperContainerComponent>
    );
}
