import {useEffect, useState} from "react";
import {Client} from "@stomp/stompjs";
import {MlModelTrainingProgress, ProjectStatusDTO} from "../../typedefs/websocket_messages";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../../typedefs/error_types";

export interface WebsocketHandlers {
    onMessage?: (data: any) => void;
    onClose?: () => void;
    onError?: (event: Event) => void;
}

export type WebSocketWithStatus = {
    socket?: WebSocket;
    stompClient?: Client;
    status: 'OPEN' | 'CLOSED' | 'ERROR';
    receivedMessages: MlModelTrainingProgress | ProjectStatusDTO | null;
};

export const useWebsocketManager = () => {
    const [sockets, setSockets] = useState<Record<string, WebSocketWithStatus>>({});
    const [lastConnectedUrl, setLastConnectedUrl] = useState<string | null>(null);
    const {showMessage} = useSnackbar();

    const connect = (url: string, handlers?: WebsocketHandlers, isStomp: boolean = false, messageOnConnect?: any, onConnected?: () => void) => {
        if (sockets[url]) {
            return;
        }

        if (isStomp) {
            const stompClient = new Client({
                brokerURL: url,
                onConnect: (frame) => {
                    if (messageOnConnect) {
                        stompClient.subscribe(`/topic/responses/${messageOnConnect}`, (message) => {
                            handlers?.onMessage?.(message.body);
                            setSockets((prevSockets) => ({
                                ...prevSockets,
                                [url]: {
                                    ...prevSockets[url],
                                    receivedMessages: JSON.parse(message.body) as ProjectStatusDTO
                                }
                            }));
                        });

                        stompClient.publish({destination: `/app/start/${messageOnConnect}`, body: messageOnConnect});
                    }
                },
                onStompError: (frame) => {
                    // @ts-ignore
                    handlers?.onError?.(frame);
                }
            });
            stompClient.activate();

            setSockets((prevSockets) => ({
                ...prevSockets,
                [url]: {
                    stompClient: stompClient,
                    status: 'OPEN',
                    receivedMessages: null
                }
            }));
            console.log(sockets[url])
        } else {
            const socket = new WebSocket(url);

            socket.onopen = (event: Event) => {
                console.log("open socket")
                if (messageOnConnect) {
                    socket.send(messageOnConnect);
                }
            };
            setSockets((prevSockets) => ({
                ...prevSockets,
                [url]: {
                    client: socket,
                    status: 'OPEN',
                    receivedMessages: null
                }
            }));

            socket.onmessage = (event) => {
                handlers?.onMessage?.(event.data);
                setSockets((prevSockets) => ({
                    ...prevSockets,
                    [url]: {
                        ...prevSockets[url],
                        receivedMessages: JSON.parse(event.data) as MlModelTrainingProgress
                    }
                }));
            };

            socket.onclose = (event: any)  => {
                handlers?.onClose?.();
            }
        }
        setLastConnectedUrl(url);
    };

    const disconnect = (url: string) => {
        if (sockets[url]?.stompClient) {
            sockets[url].stompClient!.deactivate().then(() =>
                showMessage("disconnected", SnackbarSeverity.INFO)
            );
        }
        else {
            showMessage("disconnected", SnackbarSeverity.INFO)
            // @ts-ignore
            sockets[url]?.socket.close();
        }

        const newSockets = {...sockets};
        delete newSockets[url];
        setSockets(newSockets);
    };

    const sendMessage = (url: string, message: string, connectMessage?: string) => {
        if (sockets[url]?.stompClient) {
            sockets[url].stompClient!.publish({destination: `/app/end/${connectMessage}`, body: message});
        } else {
            // @ts-ignore
            sockets[url]?.socket.send(message);
        }
    };

    useEffect(() => {
    }, [lastConnectedUrl, sockets]);

    return {
        connect,
        disconnect,
        sendMessage,
        sockets
    };
};