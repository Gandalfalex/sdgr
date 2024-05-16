package de.tudresden.sus.ports;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.inbound.dto.LogMessageDTO;
import de.tudresden.sus.adapter.inbound.dto.LogSessionDTO;
import de.tudresden.sus.adapter.outbound.entity.LogMessage;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface LogMessageServicePort {
    List<LogMessageDTO> getLogsForTrack(Long trackId);
    List<LogMessageDTO> getLogsForTrack(Long trackId, int pageNumber, int pageSize);
    void addLogsForTrack(LogMessage data);
    int countElements(Long trackId);
    void deleteOldLogs(Long trackId);
    List<LogSessionDTO> getAllSessions(Long trackId);
    JsonNode createLogGraphData(Long trackId, String sendSession);
    List<LogMessageDTO> findAnyMatching(Long trackId, String searchQuery, int pageNumber, int pageSize);
    int countElementsByQuery(Long trackId, String searchQuery);
    List<LogMessageDTO> findAllBySendSessionAndTrackId(Long trackId, String sendSession);
}
