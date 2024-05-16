package de.tudresden.sus.adapter.inbound.rest;

import de.tudresden.sus.adapter.inbound.dto.TrackDTO;
import de.tudresden.sus.adapter.outbound.entity.Track;
import de.tudresden.sus.ports.LogMessageServicePort;
import de.tudresden.sus.ports.ProjectServicePort;
import de.tudresden.sus.ports.TrackServicePort;
import io.micrometer.core.annotation.Timed;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.modelmapper.ModelMapper;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/projects/")
@Slf4j
@CrossOrigin
@RequiredArgsConstructor
public class TrackController {

    private final ModelMapper modelMapper;

    private final ProjectServicePort projectService;

    private final TrackServicePort trackService;

    private final LogMessageServicePort logMessageService;


    @GetMapping("{projectId}/tracks")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all tracks",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = TrackDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project not found"
                    )
            }
    )
    @Timed(value = "getTracks.time", description = "Time taken to get all tracks for a project")
    public ResponseEntity<List<TrackDTO>> getTracks(@PathVariable Long projectId) {
        projectService.getProjectById(projectId);

        var tracks = trackService.getAllTracksOfProject(projectId).map(track -> modelMapper.map(track, TrackDTO.class)).toList();
        log.info("found_ {}", tracks.size());
        return new ResponseEntity<>(tracks, HttpStatus.OK);
    }

    @GetMapping("{projectId}/tracks/{trackId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return track for specific id",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = TrackDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project or track not found"
                    )
            }
    )
    @Timed(value = "getTrackById.time", description = "Time taken to get a track by id")
    public ResponseEntity<TrackDTO> getTrackById(@PathVariable Long projectId, @PathVariable Long trackId) {
        var project = projectService.getProjectById(projectId);
        if (project == null) {
            log.error("project with id {} not found", projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var track = trackService.getTrackForProject(projectId, trackId);
        if (track == null) {
            log.error("track with id {} not found for project {}", trackId, projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var dto = modelMapper.map(track, TrackDTO.class);
        log.info("found_ {}", dto);
        return ResponseEntity.ok(dto);
    }

    @PostMapping("{projectId}/tracks")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "201",
                            description = "created new track",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = TrackDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project not found"
                    )
            }
    )
    @Timed(value = "createNewTrack.time", description = "Time taken to create new track")
    public ResponseEntity<TrackDTO> createNewTrack(@PathVariable Long projectId, @Valid @RequestBody TrackDTO dto) {
        var project = projectService.getProjectById(projectId);
        if (project == null) {
            log.error("project with id {} not found", projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var trackRequest = modelMapper.map(dto, Track.class);
        var track = trackService.createTrack(trackRequest);

        var projectTracks = project.getTracks();
        projectTracks.add(trackRequest);
        project.setTracks(projectTracks);

        projectService.addTrackToProject(project, track);
        log.info("updated track", dto);
        var trackResponse = modelMapper.map(track, TrackDTO.class);
        return new ResponseEntity<>(trackResponse, HttpStatus.CREATED);
    }

    @PutMapping("{projectId}/tracks/{trackId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "updated track",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = TrackDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project or track not found"
                    )
            }
    )
    @Timed(value = "updateTrack.time", description = "Time taken to update track")
    public ResponseEntity<TrackDTO> updateTrack(@PathVariable Long projectId, @PathVariable Long trackId, @Valid @RequestBody TrackDTO dto) {
        log.info("updated track");

        var project = projectService.getProjectById(projectId);
        if (project == null) {
            log.error("project with id {} not found", projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var trackRequest = modelMapper.map(dto, Track.class);
        var track = trackService.updateTrack(trackId, trackRequest);
        var trackResponse = modelMapper.map(track, TrackDTO.class);

        return ResponseEntity.ok(trackResponse);
    }

    @DeleteMapping("{projectId}/tracks/{trackId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "204",
                            description = "deleted track"
                    )
            }
    )
    @Timed(value = "deleteProject.time", description = "Time taken to delete track")
    public ResponseEntity<TrackDTO> deleteProject(@PathVariable Long projectId, @PathVariable Long trackId) {
        var project = projectService.getProjectById(projectId);
        if (project == null) {
            log.error("project with id {} not found", projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        trackService.deleteTrack(project, trackId);
        logMessageService.deleteOldLogs(trackId);
        return ResponseEntity.noContent().build();
    }

}
