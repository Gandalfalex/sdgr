import * as React from 'react';
import {useWebSocket} from './WebSocketProvider'; // Ensure path is correct
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import {MlModelTrainingProgress, ProjectStatusDTO, WebSocketMessageType} from "../../typedefs/websocket_messages";
import {LinearProgressWithLabel} from "../icons/LinearProgressChart";
import {ProjectSendingProgressChart} from "../icons/ProjectSendingProgressChart";
import {IconButton} from "@mui/material";

import InfoIcon from '@mui/icons-material/Info';

type Anchor = 'top' | 'left' | 'bottom' | 'right';


interface MessageComponentProps {
    receivedMessages: MlModelTrainingProgress | ProjectStatusDTO;
}

export default function WebSocketMessagesDrawerComponent() {
    const [state, setState] = React.useState({
        right: false
    });

    const {sockets} = useWebSocket();

    const getProjectSendingProgressChartData = (message: ProjectStatusDTO) => ({data: message});
    const getLinearProgressWithLabelData = (message: MlModelTrainingProgress) => ({value: message.progress});

    const MessageComponent: React.FC<MessageComponentProps> = ({receivedMessages}) => {
        if (!receivedMessages) return null;

        if (receivedMessages.type === WebSocketMessageType.SPRING) {
            const data = getProjectSendingProgressChartData(receivedMessages as ProjectStatusDTO);
            return <ProjectSendingProgressChart {...data} />;
        }

        if (receivedMessages.type === WebSocketMessageType.DJANGO) {
            const data = getLinearProgressWithLabelData(receivedMessages as MlModelTrainingProgress);
            return <LinearProgressWithLabel {...data} />;
        }

        return null;
    };

    const toggleDrawer =
        (anchor: Anchor, open: boolean) =>
            (event: React.KeyboardEvent | React.MouseEvent) => {
                if (
                    event.type === 'keydown' &&
                    ((event as React.KeyboardEvent).key === 'Tab' ||
                        (event as React.KeyboardEvent).key === 'Shift')
                ) {
                    return;
                }

                setState({...state, [anchor]: open});
            };

    const list = (anchor: Anchor) => (
        <Box
            sx={{width: anchor === 'top' || anchor === 'bottom' ? 'auto' : 500, marginTop: '10vh'}}
            role="presentation"
            onClick={toggleDrawer(anchor, false)}
            onKeyDown={toggleDrawer(anchor, false)}
        >
            <List>
                {Object.entries(sockets).map(([url, wsStatus]) => (
                    <React.Fragment key={url}>
                        <ListItem>
                            <ListItemText primary={`WebSocket:`}/>
                        </ListItem>
                        {wsStatus.receivedMessages && <MessageComponent receivedMessages={wsStatus.receivedMessages}/>}
                    </React.Fragment>
                ))}
            </List>
        </Box>
    );

    return (
        <div>
            <Box
                sx={{
                    position: 'fixed',
                    bottom: 0,
                    left: 0,
                    m: 3,
                }}
            >
                <IconButton onClick={toggleDrawer('right', true)}>
                    <InfoIcon fontSize="large"/>
                </IconButton>
            </Box>
            <Drawer
                anchor={'right'}
                open={state['right']}
                onClose={toggleDrawer('right', false)}
            >
                {list('right')}
            </Drawer>
        </div>
    );
}

