package de.tudresden.sus.adapter.inbound.rest;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import de.tudresden.sus.adapter.inbound.dto.PlainDataOccurrenceDTO;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSetDTO;
import de.tudresden.sus.adapter.outbound.mapper.DataMapper;
import de.tudresden.sus.ports.DataSetServicePort;
import de.tudresden.sus.ports.ProjectServicePort;
import de.tudresden.sus.ports.TrackServicePort;
import de.tudresden.sus.security.authentification.RestError;
import de.tudresden.sus.service.ProjectService;
import de.tudresden.sus.service.TrackService;
import io.micrometer.core.annotation.Timed;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import jakarta.validation.Valid;
import jakarta.validation.ValidationException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.coyote.BadRequestException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Comparator;
import java.util.List;
import java.util.Objects;

@RestController
@RequestMapping("/api/projects/")
@Slf4j
@CrossOrigin
@RequiredArgsConstructor
public class DataSetController {

    private final ProjectServicePort projectService;

    private final TrackServicePort trackService;

    private final DataSetServicePort dataSetService;

    private final DataMapper mapper;


    @GetMapping("{projectId}/tracks/{trackId}/datasets")
    @Operation(summary = "Get all foos")
    @ApiResponses( value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all dataSets",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = FloatDataSetDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project not found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getDatasets.time", description = "Time taken to return datasets")
    public ResponseEntity<List<PlainDataDTO>> getDatasets(@PathVariable Long projectId, @PathVariable Long trackId) {
        var project = projectService.getProjectById(projectId);
        var track = trackService.getTrackForProject(projectId, trackId);
        if (track == null) {
            log.error("track with id {} not found in project {}", trackId, project.getId());
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var dataSets = track.getDataSets().stream().sorted(Comparator.comparing(PlainData::getPosition)).map(mapper::toDTO).toList();
        return ResponseEntity.ok(dataSets);
    }

    @GetMapping("{projectId}/tracks/{trackId}/datasets/{datasetId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return dataset for specific id",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = FloatDataSetDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project not found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getDatasetById.time", description = "Time taken to return specific datasets")
    public ResponseEntity<PlainDataDTO> getDatasetById(@PathVariable Long projectId, @PathVariable Long trackId, @PathVariable Long datasetId) {
        var project = projectService.getProjectById(projectId);
        var track = trackService.getTrackForProject(projectId, trackId);
        var dataset = dataSetService.getDatasetForTrack(track, datasetId);
        if (dataset == null) {
            log.error("dataset with id {} not part of track {} project {}", datasetId, trackId, project.getId());
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return ResponseEntity.ok(dataset);
    }

    @PostMapping("{projectId}/tracks/{trackId}/datasets")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "201",
                            description = "created new DataSets",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = FloatDataSetDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project not found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    ),
                    @ApiResponse(
                            responseCode = "406",
                            description = "DataType not allowed",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "createNewDataSet.time", description = "Time taken to create new datasets")
    public ResponseEntity<PlainDataDTO> createNewDataSet(@PathVariable Long projectId, @PathVariable Long trackId, @Valid @RequestBody PlainDataDTO dto) {
        log.info("{}", dto);
        var project = projectService.getProjectById(projectId);
        var track = trackService.getTrackForProject(projectId, trackId);
        var dataType = track.getAllowedDataTypes().stream()
                .filter(type -> dto.getDataType().equals(type.getType())).findAny().orElseThrow(() -> new ValidationException("Datatype not allowed"));
        if (dataType == null) {
            log.error("datatype: {} not allowed in project {}", dto.getDataType(), project.getId());
            return new ResponseEntity<>(HttpStatus.NOT_ACCEPTABLE);
        }


        // get larger or negative values
        if (dto.getPosition() == null || dto.getPosition() > track.getDataSets().size() || dto.getPosition() < 0) {
            dto.setPosition(track.getDataSets().size());
        } else {
            track.getDataSets().forEach(d -> {
                if (d.getPosition() >= dto.getPosition()) {
                    d.setPosition(d.getPosition() + 1);
                }
            });
        }

        var dataSet = mapper.toEO(dto);
        dataSet = dataSetService.merge(dataSet);
        trackService.addPlainDataSetToTrack(track, dataSet);

        return new ResponseEntity<>(mapper.toDTO(dataSet), HttpStatus.CREATED);
    }

    @PutMapping("{projectId}/tracks/{trackId}/datasets/{datasetId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "updated DataSets",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = FloatDataSetDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project not found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "updateDataSet.time", description = "Time taken to update datasets")
    public ResponseEntity<PlainDataDTO> updateDataSet(@PathVariable Long projectId, @PathVariable Long trackId, @PathVariable Long datasetId, @Valid @RequestBody PlainDataDTO dto) {

        var project = projectService.getProjectById(projectId);
        if (project == null) {
            log.error("project {} not found", projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var track = trackService.getTrackForProject(projectId, trackId);
        if (track == null) {
            log.error("track {} not found in project {}", trackId, projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var dataset = dataSetService.getDatasetForTrack(track, datasetId);
        if (dataset == null) {
            log.error("dataset {} not found in track {} in project {}", datasetId, trackId, projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        int oldPos = dataset.getPosition();
        int newPos = dto.getPosition();
        // change only if needed
        if (oldPos != newPos && newPos < track.getDataSets().size() && newPos >= 0) {
            int moveTowardsNew = (oldPos > newPos) ? 1 : -1;
            // all datasets between old and new move by either + or - 1
            track.getDataSets().forEach(d -> {
                if (d.getPosition() == oldPos) {
                    d.setPosition(newPos);
                    dataSetService.merge(d);
                } else if (d.getPosition() >= Math.min(oldPos, newPos) && d.getPosition() <= Math.max(oldPos, newPos)) {
                    d.setPosition(d.getPosition() + moveTowardsNew);
                    dataSetService.merge(d);
                }
            });
        } else {
            dto.setPosition(oldPos);
            dataSetService.merge(dto);
        }
        // not beautiful, but works for now
        var response = track.getDataSets().stream().filter(d -> (Objects.equals(d.getId(), datasetId))).toList().get(0);
        return ResponseEntity.ok(mapper.toDTO(response));
    }

    @DeleteMapping("{projectId}/tracks/{trackId}/datasets/{datasetId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "204",
                            description = "deleted DataSets"
                    )
            }
    )
    @Timed(value = "deleteDataSet.time", description = "Time taken to delete datasets")
    public ResponseEntity<PlainDataDTO> deleteDataSet(@PathVariable Long projectId, @PathVariable Long trackId, @PathVariable Long datasetId) {
        var project = projectService.getProjectById(projectId);
        var track = trackService.getTrackForProject(project.getId(), trackId);
        var dataset = dataSetService.getDatasetForTrack(track, datasetId);
        dataSetService.deleteDataSet(track, dataset);
        return ResponseEntity.noContent().build();
    }


    @GetMapping("{projectId}/tracks/{trackId}/datasets/{datasetId}/preview")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "preview of dataset",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = JsonNode.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "cannot create preview",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "previewDataSet.time", description = "Time taken to get preview")
    public ResponseEntity<JsonNode> getPreview(@PathVariable Long projectId, @PathVariable Long trackId, @PathVariable Long datasetId) {
        var project = projectService.getProjectById(projectId);
        if (project == null) {
            log.error("project {} not found", projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var track = trackService.getTrackForProject(projectId, trackId);
        if (track == null) {
            log.error("track {} not found in project {}", trackId, projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var dataset = dataSetService.getDatasetForTrack(track, datasetId);
        if (dataset == null) {
            log.error("dataset {} not found in track {} in project {}", datasetId, trackId, projectId);
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        var preview = dataSetService.getPreviewData(mapper.toEO(dataset));

        return ResponseEntity.ok(preview);
    }

    @GetMapping("ml/datasets/{id}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "information where the ml configuration is implemented",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = PlainDataOccurrenceDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "dataset does not exist",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getAllMLDataSets.time", description = "Time taken to get preview")
    public ResponseEntity<List<PlainDataOccurrenceDTO>> getAllMLDataSets(@PathVariable Long id) {
        var data = dataSetService.findAllMlDataSetsForConfigurationId(id);
        return ResponseEntity.ok(data);
    }

    @GetMapping("tsd/datasets/{id}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "information where the tsd configuration is implemented",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = PlainDataOccurrenceDTO.class)
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "project not found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getAllTSDDataSets.time", description = "Time to find all occurrences of tsd usages")
    public ResponseEntity<List<PlainDataOccurrenceDTO>> getAllTSDDataSets(@PathVariable Long id) {
        var data = dataSetService.findAllTSDDataSetsForConfigurationId(id);
        return ResponseEntity.ok(data);
    }
}


