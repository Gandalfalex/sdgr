---
title: "WebSocket Requests Management"
date: 2023-12-08T19:22:33+01:00
tags: [websocket, messaging, project management, real-time communication]
featured_image: ""
description: "This guide provides instructions on how to manage WebSocket requests in the application, including starting and stopping message streams for specific projects."
---

## Managing WebSocket Requests

This documentation covers the procedures for starting and stopping WebSocket requests in the application. The WebSocketController handles real-time communication for project-specific tasks.

{{<mermaid align="left">}}
graph 
    A[WebSocketController] -->|Start/Stop Commands| B[ThreadHolder]
    B -->|Manage Threads| C[SendDataThread]
    C -->|Send Data & Status Updates| D[KafkaTemplate]
    C -->|Emit WebSocket Events| E[WebSocketEventService]
    E -->|Stream of Project Status| A
{{< /mermaid >}}


### Starting WebSocket Requests

To initiate a WebSocket request for a specific project:

1. **Send a Start Message**: Use the `/start/{message}` WebSocket endpoint, where `{message}` is the project ID you want to start.

    ```javascript
    stompClient.send("/start/{projectId}", {}, {});
    ```

    - `projectId`: Replace with the actual project ID.
    - The server will process this message and start the relevant tasks for the project.

2. **Handle Responses**: Listen to the `/topic/responses/{projectId}` topic to receive real-time updates and responses from the server.

    ```javascript
    stompClient.subscribe('/topic/responses/' + projectId, function (response) {
        // Handle the response here
    });
    ```

3. **Confirm Start**: You should receive a confirmation message with the status, indicating that the sending of messages has started.

### Stopping WebSocket Requests

To stop an ongoing WebSocket request for a project:

1. **Send a Stop Message**: Use the `/end/{message}` WebSocket endpoint, where `{message}` is the project ID you want to stop.

    ```javascript
    stompClient.send("/end/{projectId}", {}, {});
    ```

    - `projectId`: Replace with the actual project ID.
    - The server will process this message and stop the tasks associated with the project.

2. **Confirmation**: The server will confirm that the tasks have been stopped, and you should no longer receive updates for the specified project ID.

### Error Handling

- **Invalid Project ID**: If the project ID is invalid or not found, the server will respond with an error message.
- **Already Running/Stopped Tasks**: If the tasks for the project are already in the desired state (running or stopped), the server will respond with an appropriate message.

---

*Note: Replace `{projectId}` with the actual numeric ID of the project you wish to control. Adjust the JavaScript snippets according to your client-side WebSocket implementation.*
