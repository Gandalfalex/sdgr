import React, {useEffect, useState} from "react";
import {IconButton, ListItemIcon, TextField, Tooltip, Typography} from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import {MlConfig} from "../../typedefs/django_types";
import {createTrainingWebSocket} from "../../api/DjangoAPI";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../../typedefs/error_types";
import {useWebSocket} from "../websockets/WebSocketProvider";
import {ProgressWithPercent} from "../icons/CircularProgressCustomIcon";
import {useTranslation} from "react-i18next";


interface TrainProps {
    id: number,
    modelId: number,
    solution: MlConfig,
    onUpdate: () => void;
}

export const StartTrainElement = (props: TrainProps) => {

    const {id, modelId, solution, onUpdate} = props;
    const [iterations, setIterations] = useState(100);
    const [accuracy, setAccuracy] = useState(0.9);
    const [isClicked, setIsClicked] = useState(false);
    const [status, setStatus] = useState('IN_PROGRESS');
    const [percentage, setPercentage] = useState<number>(0);
    const {showMessage} = useSnackbar();
    const {connect} = useWebSocket();
    const { t } = useTranslation(['dialogs', 'headers']);


    const handleOpen = () => {
        setIsClicked(true);
        const message = `{"iterations": ${iterations}, "accuracy": ${accuracy}}`;
        connect(createTrainingWebSocket(modelId, id), {
            onMessage: handleWebsocketMessage,
            onClose: handleClose,
            onError: handleError
        }, false, message);

        showMessage(t('ml_start_training', {ns: ['dialogs']}), SnackbarSeverity.INFO);
    };

    const handleWebsocketMessage = (data: string) => {
        try {
            const dataObject = JSON.parse(data);
            if (dataObject.progress != null) {
                setPercentage(dataObject.progress);
            }
        } catch (error) {
            console.error("Error parsing JSON:", error);
        }
    };

    const handleClose = () => {
        setStatus("close");
        setPercentage(0);
        setIsClicked(false);
        showMessage(t('ml_finished_training', {ns: ['dialogs']}), SnackbarSeverity.SUCCESS);
        onUpdate()
    };

    const handleError = (event: Event) => {
        showMessage(t('ml_error_event', {ns: ['dialogs']}) + event, SnackbarSeverity.ERROR);
    };


    const handleIterationsChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (!isNaN(Number(event.target.value)) || event.target.value === "") {
            setIterations(Number(event.target.value));
        }
    };

    const handleAccuracyChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (!isNaN(Number(event.target.value)) || event.target.value === "") {
            setAccuracy(Number(event.target.value));
        }
    };

    useEffect(() => {
        if (solution.is_running !== null) {
            setIsClicked(true)
        } else {
            setIsClicked(false)
        }
    }, [id, modelId, status]);
    return (<div>
            <Typography variant="h6"> {t('ml_start_train_information', {ns: ['dialogs']})} Add specific options for training</Typography>
            <ListItemIcon style={{display: 'flex', justifyContent: 'flex-end'}}>
                <Tooltip title={!solution.is_running !== null ? t('ml_start_train_tooltip', {ns: ['dialogs']}) : t('ml_is_training_tooltip', {ns: ['dialogs']})}
                         arrow>
                    <IconButton className={'growButton'} onClick={() => handleOpen()}>
                        {isClicked
                            ? <ProgressWithPercent percentage={percentage}/>
                            : <PlayArrowIcon/>}
                    </IconButton>
                </Tooltip>
            </ListItemIcon>
            <div style={{marginTop: '16px'}}>
                <TextField
                    type="number"
                    label="Iterations"
                    value={iterations}
                    onChange={handleIterationsChange}
                    InputProps={{
                        inputProps: {
                            step: "1"
                        }
                    }}
                    variant="outlined"
                    fullWidth
                />
            </div>

            <div style={{marginTop: '16px'}}>
                <TextField
                    type="number"
                    label="Loss"
                    value={accuracy}
                    onChange={handleAccuracyChange}
                    InputProps={{
                        inputProps: {
                            step: "0.01"
                        }
                    }}
                    variant="outlined"
                    fullWidth
                />
            </div>
        </div>
    );
}
