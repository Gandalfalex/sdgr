import React, { createContext, useContext, ReactNode } from 'react';
import {useWebsocketManager, WebsocketHandlers, WebSocketWithStatus} from "./WebsocketManager";

type WebSocketContextType = {
    connect: (url: string, handlers?: WebsocketHandlers, isStomp?:boolean,  messageOnConnect?: any,  onConnected?: () => void) => void;
    disconnect: (url: string) => void;
    sendMessage: (url: string, message: string, connectMessage?: string) => void;
    sockets: Record<string, WebSocketWithStatus>;
};

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

interface WebSocketProviderProps {
    children: ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ children }) => {
    const wsManager = useWebsocketManager();

    return (
        <WebSocketContext.Provider value={wsManager}>
            {children}
        </WebSocketContext.Provider>
    );
};

export const useWebSocket = () => {
    const context = useContext(WebSocketContext);
    if (context === undefined) {
        throw new Error('useWebSocket must be used within a WebSocketProvider');
    }
    return context;
};
