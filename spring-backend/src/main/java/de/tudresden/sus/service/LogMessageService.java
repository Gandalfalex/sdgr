package de.tudresden.sus.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import de.tudresden.sus.adapter.inbound.dto.LogMessageDTO;
import de.tudresden.sus.adapter.inbound.dto.LogSessionDTO;
import de.tudresden.sus.adapter.outbound.entity.LogMessage;
import de.tudresden.sus.adapter.outbound.repositories.LogMessageRepository;
import de.tudresden.sus.ports.LogMessageServicePort;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class LogMessageService implements LogMessageServicePort {

    private final LogMessageRepository repository;

    /**
     * get all logs for given track
     *
     * @param trackId
     * @return
     */
    public List<LogMessageDTO> getLogsForTrack(Long trackId) {

        var logs = repository.findByTrackId(trackId);
        if (logs.isEmpty()) {
            return null;
        }
        return toDTO(logs);
    }

    /**
     * get all logs belonging to a track, paging optional
     *
     * @param trackId
     * @param pageNumber
     * @param pageSize
     * @return
     */
    public List<LogMessageDTO> getLogsForTrack(Long trackId, int pageNumber, int pageSize) {
        if (pageSize <= 1) {
            log.error("pagesize has to be larger than 1, pagesize: {}", pageSize);
            return null;
        }
        var logs = repository.findByTrackId(trackId, PageRequest.of(pageNumber, pageSize));
        if (logs.isEmpty()) {
            log.info("no logs found");
            return null;
        }
        return toDTO(logs.getContent());
    }

    public void addLogsForTrack(LogMessage data) {
        repository.saveAndFlush(data);
    }

    public int countElements(Long trackId) {
        return repository.countByTrackId(trackId);
    }

    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public void deleteOldLogs(Long trackId) {
        repository.deleteAllByTrackId(trackId);
    }


    /**
     * Return a list of all session, each distinct
     *
     * @param trackId
     * @return
     */
    public List<LogSessionDTO> getAllSessions(Long trackId) {
        return repository.findAllSessionsByTrackId(trackId).stream().map(t -> new LogSessionDTO().setSession(t)).toList();
    }

    public List<LogMessageDTO> findAllBySendSessionAndTrackId(Long trackId, String sendSession) {
        return toDTO(repository.findAllByTrackIdAndSendSession(trackId, sendSession));
    }

    /**
     * create a json node with values and labels for graph representation
     *
     * @param trackId
     * @param sendSession
     * @return
     */
    public JsonNode createLogGraphData(Long trackId, String sendSession) {
        var node = JsonNodeFactory.instance.objectNode();
        var labels = JsonNodeFactory.instance.arrayNode();
        var values = JsonNodeFactory.instance.arrayNode();
        var logs = repository.findAllByTrackIdAndSendSession(trackId, sendSession);

        if (!logs.isEmpty()) {
            // calculate difference between local time and utc time, add/remove difference since js library does not care
            // for timezones. A bit hacky but works
            var timeOffset = ZoneId.systemDefault().getRules().getOffset(Instant.now()).getTotalSeconds() * 1000;
            logs.forEach(temp -> {
                values.add(toFloat(temp.getMessage()));
                var time = temp.getTimeStamp().toEpochMilli() - timeOffset;
                labels.add(time);
            });
            node.set("labels", labels);
            node.set("values", values);
            log.info("nodes created");
            return node;
        }
        return null;
    }

    /**
     * find elements matching the search query, paging optional
     *
     * @param trackId
     * @param searchQuery
     * @param pageNumber
     * @param pageSize
     * @return
     */
    public List<LogMessageDTO> findAnyMatching(Long trackId, String searchQuery, int pageNumber, int pageSize) {
        var page = PageRequest.of(pageNumber, pageSize);
        return pageSize >= 0
                ? toDTO(repository.findByQueryWithPage(trackId, searchQuery, page).getContent())
                : toDTO(repository.findByQuery(trackId, searchQuery));
    }

    /**
     * count elements matching the query
     *
     * @param trackId
     * @param searchQuery
     * @return
     */
    public int countElementsByQuery(Long trackId, String searchQuery) {
        return repository.countBySearchQuery(trackId, searchQuery);
    }

    @SneakyThrows
    private float toFloat(String s) {
        return Float.parseFloat(s.split(" ")[0]);
    }

    @SneakyThrows
    private List<LogMessageDTO> toDTO(List<LogMessage> logs) {
        return logs
                .stream()
                .map(log -> {
                            var instant = log.getTimeStamp();
                            return new LogMessageDTO()
                                    .setMessage(log.getMessage())
                                    .setTime(LocalDateTime.ofInstant(instant, ZoneId.of("UTC")).format(DateTimeFormatter.ofPattern("HH:mm:ss:SSS")))
                                    .setDataSetName(log.getDataSetName())
                                    .setSendSession(log.getSendSession());
                        }
                )
                .toList();
    }
}
