package de.tudresden.sus.adapter.inbound.websocket;

import de.tudresden.sus.adapter.inbound.dto.ProjectStatusDTO;
import de.tudresden.sus.adapter.inbound.errorhandler.InvalidCredentialException;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.repositories.ProjectRepository;
import de.tudresden.sus.adapter.outbound.repositories.UserRepository;
import de.tudresden.sus.ports.ProjectServicePort;
import jakarta.persistence.EntityNotFoundException;
import java.util.HashMap;
import java.util.Map;
import java.util.Objects;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.event.EventListener;
import org.springframework.messaging.handler.annotation.DestinationVariable;
import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.simp.SimpMessageHeaderAccessor;
import org.springframework.messaging.simp.SimpMessagingTemplate;
import org.springframework.messaging.simp.stomp.StompHeaderAccessor;
import org.springframework.stereotype.Controller;
import org.springframework.web.socket.messaging.SessionConnectEvent;
import org.springframework.web.socket.messaging.SessionDisconnectEvent;
import reactor.core.Disposable;

/**
 * Controller for managing WebSocket connections and messaging in a Spring application.
 * Handles the flow of starting and stopping tasks related to projects through WebSocket messages.
 */
@Controller
@Slf4j
@RequiredArgsConstructor
public class WebSocketController {

    private final ProjectRepository repository;
    private final UserRepository userRepository;
    private final ProjectServicePort projectService;
    private final WebSocketEventService webSocketEventService;
    private final SimpMessagingTemplate messagingTemplate;

    private final Map<Long, Disposable> activeSubscriptions = new HashMap<>();

    /**
     * Processes a message from a client to start sending messages to the kafka broker.
     *
     * @param message The project ID obtained from the message path.
     * @param headerAccessor Accessor for WebSocket message headers to retrieve user information.
     * @return ProjectStatusDTO containing the status of the action, like starting a task.
     * @throws Exception if user is not found or there is an issue with project retrieval.
     */
    @MessageMapping("/start/{message}")
    public ProjectStatusDTO processMessageFromClient(
        @DestinationVariable Long message,
        SimpMessageHeaderAccessor headerAccessor
    ) throws Exception {
        log.info("received message: {}", message);

        String userEmail = (String) Objects.requireNonNull(
            headerAccessor.getSessionAttributes()
        ).get("user");
        headerAccessor.getSessionId();
        User user = userRepository
            .findByEmail(userEmail)
            .orElseThrow(() -> new InvalidCredentialException("user not found")
            );

        var project = repository
            .findByIdAndUser(message, user)
            .orElseThrow(() ->
                new EntityNotFoundException("cannot find project")
            );
        if (project == null) {
            log.error("project with id {} not found", message);
            return new ProjectStatusDTO().setMessage("Project not found");
        }

        if (activeSubscriptions.containsKey(project.getId())) {
            log.info(
                "Task already running for project id: {}",
                project.getId()
            );
            return new ProjectStatusDTO().setMessage("Task already running");
        }

        Disposable subscription = webSocketEventService
            .getEventStream((project.getId()))
            .subscribe(event ->
                messagingTemplate.convertAndSend(
                    "/topic/responses/" + project.getId(),
                    event
                )
            );

        log.info("id of current object: {}", project.getId());
        activeSubscriptions.put(project.getId(), subscription);
        projectService.startMessageSending(project, user.getEmail());
        return new ProjectStatusDTO().setMessage("Starting to Send");
    }

    /**
     * Processes a message from a client to stop the ongoing message sending.
     *
     * @param message The project ID obtained from the message path.
     * @param headerAccessor Accessor for WebSocket message headers to retrieve user information.
     * @return ProjectStatusDTO containing the status of the action, like stopping a task.
     * @throws Exception if there is an issue with accessing the project or user data.
     */
    @MessageMapping("/end/{message}")
    public ProjectStatusDTO processKillMessageFromClient(
        @DestinationVariable Long message,
        SimpMessageHeaderAccessor headerAccessor
    ) throws Exception {
        Disposable subscription = activeSubscriptions.remove(message);
        log.info("killing messages");
        String userEmail = (String) headerAccessor
            .getSessionAttributes()
            .get("user");
        User user = userRepository.findByEmail(userEmail).orElse(null);

        var project = repository.findByIdAndUser(message, user).orElse(null);
        projectService.stopMessageSending(project);

        if (subscription != null && !subscription.isDisposed()) {
            subscription.dispose();
            log.info("Task with id {} killed", message);
            return new ProjectStatusDTO().setMessage("Task killed");
        } else {
            log.error("Task with id {} not found or already killed", message);
            return new ProjectStatusDTO()
                .setMessage("Task not found or already killed");
        }
    }

    @EventListener
    public void handleWebSocketConnectListener(SessionConnectEvent event) {
        StompHeaderAccessor headerAccessor = StompHeaderAccessor.wrap(
            event.getMessage()
        );
        String userEmail = (String) headerAccessor
            .getSessionAttributes()
            .get("user");
    }

    @EventListener
    public void handleWebSocketDisconnectListener(
        SessionDisconnectEvent event
    ) {
        StompHeaderAccessor headerAccessor = StompHeaderAccessor.wrap(
            event.getMessage()
        );
        String userEmail = (String) headerAccessor
            .getSessionAttributes()
            .get("user");
    }
}
