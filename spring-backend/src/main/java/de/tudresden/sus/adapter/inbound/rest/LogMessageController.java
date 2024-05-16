package de.tudresden.sus.adapter.inbound.rest;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.inbound.dto.LogMessageDTO;
import de.tudresden.sus.adapter.inbound.dto.LogSessionDTO;
import de.tudresden.sus.ports.LogMessageServicePort;
import de.tudresden.sus.service.LogMessageService;
import io.micrometer.core.annotation.Timed;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/logs/")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin
public class LogMessageController {

    private final LogMessageServicePort logMessageService;

    @GetMapping("{trackId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return logs for specific track",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = LogMessageDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no logs found, return empty list",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = LogMessageDTO.class)
                            )
                    )
            }
    )
    @Timed(value = "getLogsForTrack.time", description = "Time taken to get logs for track")
    public ResponseEntity<List<LogMessageDTO>> getLogsForTrack(@PathVariable Long trackId,
                                                               @RequestParam(name = "page_size", required = false) Integer pageSize,
                                                               @RequestParam(name = "page_number", required = false) Integer pageNumber,
                                                               @RequestParam(name = "search_query", required = false) String searchQuery) {
        var isPageable = !(pageSize == null || pageSize <= 0);
        var isSearchable = (!searchQuery.isEmpty() || !searchQuery.isBlank()) && !searchQuery.equals("null");

        List<LogMessageDTO> logs;
        if (!isSearchable && !isPageable){
            logs = logMessageService.getLogsForTrack(trackId);
        }
        else if (isSearchable){
            logs = logMessageService.findAnyMatching(trackId, searchQuery, (pageNumber == null) ? 0 : pageNumber, pageSize);
        }
        else {
            logs = logMessageService.getLogsForTrack(trackId, (pageNumber == null) ? 0 : pageNumber, pageSize);
        }


        return new ResponseEntity<>(logs, HttpStatus.OK);
    }

    @GetMapping("{trackId}/log_size")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return the number of logs for the given track",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = Integer.class)
                            )
                    )
            }
    )
    @Timed(value = "getLogSize.time", description = "Time taken to get calculate the log size")
    public ResponseEntity<Integer> getLogSize(@PathVariable Long trackId,  @RequestParam(name = "search_query", required = false) String searchQuery) {
        var isSearchable = (searchQuery != null && (!searchQuery.isEmpty() || !searchQuery.isBlank()));
        if (isSearchable){
            return new ResponseEntity<>(logMessageService.countElementsByQuery(trackId, searchQuery), HttpStatus.OK);
        }
        return new ResponseEntity<>(logMessageService.countElements(trackId), HttpStatus.OK);
    }

    @GetMapping("{trackId}/logSessions")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return the list of logSessions",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = LogMessageDTO.class)
                            )
                    )
            }
    )
    @Timed(value = "getLogSessions.time", description = "Time taken to get logs for session")
    public ResponseEntity<List<LogSessionDTO>> getLogSessions(@PathVariable Long trackId) {
        return new ResponseEntity<>(logMessageService.getAllSessions(trackId), HttpStatus.OK);
    }

    @GetMapping("{trackId}/logSession")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return all logs for one session",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = LogMessageDTO.class)
                            )
                    )
            }
    )
    @Timed(value = "getAllByLogSession.time", description = "Time taken to get all logs for session")
    public ResponseEntity<List<LogMessageDTO>> getAllByLogSession(@PathVariable Long trackId, @RequestParam(name = "session", required = false) String logSession) {
        return new ResponseEntity<>(logMessageService.findAllBySendSessionAndTrackId(trackId, logSession), HttpStatus.OK);
    }

    @GetMapping("{trackId}/logGraph")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return a graph for one session",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = LogMessageDTO.class)
                            )
                    )
            }
    )
    @Timed(value = "getLogGraph.time", description = "Time taken to get log graph")
    public ResponseEntity<JsonNode> getLogGraph(@PathVariable Long trackId, @RequestParam(name = "session", required = false) String logSession) {
        return new ResponseEntity<>(logMessageService.createLogGraphData(trackId, logSession), HttpStatus.OK);
    }
}
