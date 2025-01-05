package de.tudresden.sus.datagenerator.sender;

import de.tudresden.sus.adapter.inbound.websocket.WebSocketEventService;
import de.tudresden.sus.adapter.outbound.domain_objects.TrackDO;
import de.tudresden.sus.service.LogMessageService;
import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class ThreadOrganizer {

    private final KafkaTemplate template;
    private final ThreadHolder threadHolder;
    private final LogMessageService logMessageService;
    private final WebSocketEventService eventService;

    /**
     * create a new thread and start sending
     *
     * @param track
     * @param id
     */
    public void runConfigDataSetThreads(TrackDO track, long id) {
        var temp = new SendDataThread(track, id, template, logMessageService, eventService);
        threadHolder.startThread(temp);
    }

    /**
     * stop all threads belonging to a  given project id
     *
     * @param id
     */
    public void stopThreads(long id) {
        threadHolder.stopThreads(id);
    }


    public boolean checkIfRunning(Long id) {
        return ThreadHolder.isRunning(id);
    }
}
