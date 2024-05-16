package de.tudresden.sus.adapter.inbound.websocket;

import de.tudresden.sus.adapter.inbound.dto.ProjectStatusDTO;
import de.tudresden.sus.adapter.inbound.dto.TrackStatusDTO;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.DirectProcessor;
import reactor.core.publisher.Flux;
import reactor.core.publisher.FluxSink;

import java.time.Instant;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.CopyOnWriteArrayList;


/**
 * Service class for handling WebSocket events related to project statuses.
 * Manages the emission and removal of events in a thread-safe manner.
 */
@Service
@Slf4j
public class WebSocketEventService {

    private final DirectProcessor<ProjectStatusDTO> processor = DirectProcessor.create();
    private Map<Long, ProjectStatusDTO> events = new ConcurrentHashMap<>();
    private final FluxSink<ProjectStatusDTO> sink = processor.sink();

    /**
     * Emits a new event associated with a specific project.
     * If an event for the given project ID does not exist, it creates a new one;
     * otherwise, updates the existing event.
     *
     * @param projectId The ID of the project associated with the event.
     * @param event The track status details to be added or updated.
     */
    public synchronized void emitEvent(Long projectId, TrackStatusDTO event) {
        if (events.get(projectId) == null) {
            var tracks = new CopyOnWriteArrayList<TrackStatusDTO>();
            tracks.add(event);
            events.put(projectId, new ProjectStatusDTO().setStatus("running")
                    .setStartTime(Instant.now().toString())
                    .setId(projectId)
                    .setRunningTracks(tracks));
        } else {
            events.get(projectId).updateOrAdd(event);
        }
        sink.next(events.get(projectId));
    }

    /**
     * Removes all events associated with the specified project ID.
     *
     * @param id The ID of the project whose events are to be removed.
     */
    public void remove(Long id) {
        events.remove(id);
    }

    /**
     * Removes a specific track status from the events associated with a given project ID.
     *
     * @param id The ID of the project.
     * @param dto The track status to be removed.
     */
    public void removeTrack(Long id, TrackStatusDTO dto) {
        events.get(id).getRunningTracks().remove(dto);
    }

    /**
     * Provides a stream of project status events for a specific project ID.
     *
     * @param id The ID of the project for which events are to be streamed.
     * @return Flux<ProjectStatusDTO> Stream of project status events.
     */
    public Flux<ProjectStatusDTO> getEventStream(Long id) {
        log.info("id: {}", id);
        return processor.filter(event -> event.getId().equals(id));
    }
}