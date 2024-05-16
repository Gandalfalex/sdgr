package de.tudresden.sus.datagenerator.sender;

import de.tudresden.sus.adapter.inbound.dto.TrackStatusDTO;
import de.tudresden.sus.adapter.inbound.websocket.WebSocketEventService;
import de.tudresden.sus.adapter.outbound.domain_objects.DataSetDO;
import de.tudresden.sus.adapter.outbound.domain_objects.TrackDO;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.LogMessage;
import de.tudresden.sus.datagenerator.kafka.KafkaMessageHolder;
import de.tudresden.sus.ports.LogMessageServicePort;
import de.tudresden.sus.service.LogMessageService;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.kafka.core.KafkaTemplate;

import java.beans.PropertyChangeListener;
import java.beans.PropertyChangeSupport;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;


/**
 * A custom thread class for sending data related to a specific track.
 * Handles data transmission using Kafka and updates track status through WebSocket events.
 */
@Getter
@Slf4j
public class SendDataThread extends Thread {

    private final LogMessageServicePort service;

    private final TrackDO track;

    private final Long uuid;

    private final KafkaTemplate<String, KafkaMessageHolder> template;

    private final PropertyChangeSupport support;

    private final WebSocketEventService webSocketEventService;

    /**
     * Constructs a SendDataThread with specified parameters.
     *
     * @param track The track data object containing information to be sent.
     * @param projectId The unique identifier of the project associated with this thread.
     * @param template The Kafka template used for sending messages.
     * @param service The service for logging messages.
     * @param webSocketEventService The service for emitting WebSocket events.
     */
    public SendDataThread(TrackDO track, long projectId, KafkaTemplate<String, KafkaMessageHolder> template, LogMessageService service, WebSocketEventService webSocketEventService) {
        this.track = track;
        support = new PropertyChangeSupport(this);
        this.uuid = projectId;
        this.template = template;
        this.service = service;
        this.webSocketEventService = webSocketEventService;
    }

    /**
     * The main execution method for the thread.
     * Handles sending of data, updates track status, and manages sleep interruptions.
     */
    @Override
    public void run() {
        String sendSession = LocalDateTime.ofInstant(Instant.now(), ZoneOffset.UTC).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"));

        TrackStatusDTO trackStatus = new TrackStatusDTO().setTrackName(track.getName()).setId(track.getId());
        var sender = new KafkaMessageHolder()
                .setUnit(track.getUnit())
                .setTrackId(track.getId())
                .setTrackName(track.getName());

        do {
            for (DataSetDO value : track.getDatasets()) {
                var sleepMs = (long) (1000d / value.getFrequency());

                trackStatus.setProgress(((float) (value.getPosition() + 1) / track.getDatasets().size()) * 100);
                webSocketEventService.emitEvent(uuid, trackStatus.setDataSetName(value.getName()));

                if (value.getType().equals(DataTypes.SLEEP)) {
                    try {
                        log.info("sleeping for {}ms", 1000 * value.getSleepTime());
                        sleep((1000L * value.getSleepTime()));
                    } catch (InterruptedException e) {
                        template.destroy();
                        support.firePropertyChange(String.valueOf(uuid), null, this);
                        log.error("sleep threw error: {}", e.getMessage());
                        interrupt();
                        return;
                    }
                } else {
                    for (String messageValue : value.getValues()) {
                        var message = String.format("%s %s", messageValue, track.getUnit());

                        template.send(String.valueOf(uuid), sender.setValue(messageValue));
                        var logMessage = new LogMessage()
                                .setTrackId(getTrack().getId())
                                .setSendSession(sendSession)
                                .setDataSetName(value.getName()).setMessage(message).setTimeStamp(Instant.now());
                        service.addLogsForTrack(logMessage);

                        try {
                            sleep(sleepMs);
                        } catch (InterruptedException e) {
                            template.destroy();
                            support.firePropertyChange(String.valueOf(uuid), null, this);
                            log.error("sleep threw error: ", e);
                            interrupt();
                            return;
                        }
                    }
                }
                if (Thread.currentThread().isInterrupted()) {
                    return;
                }
            }
        }
        while (track.isRepeating() && !Thread.currentThread().isInterrupted());
        template.destroy();
        webSocketEventService.removeTrack(uuid, trackStatus);
        support.firePropertyChange(String.valueOf(uuid), null, this);
    }

    /**
     * Adds a property change listener to this thread.
     * Listeners are notified of changes in thread properties, like status changes.
     *
     * @param pcl The property change listener to add.
     */
    public void addPropertyChangeListener(PropertyChangeListener pcl) {
        support.addPropertyChangeListener(pcl);
    }

    /**
     * Removes a property change listener from this thread.
     *
     * @param pcl The property change listener to remove.
     */
    public void removePropertyChangeListener(PropertyChangeListener pcl) {
        support.removePropertyChangeListener(pcl);
    }

    /**
     * Interrupts the current thread, stopping the sending process and cleaning up resources.
     */
    @Override
    public void interrupt() {
        super.interrupt();
        template.destroy();
        log.info("stopped sending {}", track.getName());
    }

    @Override
    public String toString() {
        return "{" +
                "SendDataThread: " + uuid +
                ", name: " + track.getName() +
                "}";
    }
}
