package de.tudresden.sus.adapter.inbound.rest;

import de.tudresden.sus.adapter.outbound.restclient.models.dto.*;
import de.tudresden.sus.security.authentification.RestError;
import de.tudresden.sus.service.DjangoRestService;
import io.micrometer.core.annotation.Timed;
import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import lombok.NonNull;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/django/")
@Slf4j
@CrossOrigin
@RequiredArgsConstructor
public class DjangoRestController {


    private final DjangoRestService service;

    @GetMapping("/ml")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all models",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = MLModelsDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid ml model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getModels.time", description = "Time taken to find all Models")
    public ResponseEntity<List<MLModelsDTO>> getMLModels() {
        var models = service.findAllMLModels();

        return models == null || models.isEmpty()
                ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
                : new ResponseEntity<>(models, HttpStatus.OK);
    }

    @GetMapping("/ml/configured")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all models",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = MLModelsDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid ml model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getModels.time", description = "Time taken to find all Models")
    public ResponseEntity<List<MLModelsDTO>> getMLModelsWithConfig() {
        var models = service.findAllMLModelsWithConfiguration();

        return models == null || models.isEmpty()
                ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
                : new ResponseEntity<>(models, HttpStatus.OK);
    }

    @GetMapping("/tsd")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all models",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = MLModelsDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid tsd model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getModels.time", description = "Time taken to find all Models")
    public ResponseEntity<List<TSDModelDTO>> getTSDModels() {
        var models = service.findAllTSDModels();

        return models == null || models.isEmpty()
                ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
                : new ResponseEntity<>(models, HttpStatus.OK);
    }

    @GetMapping("/tsd/configured")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all models",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = MLModelsDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid tsd model found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getModels.time", description = "Time taken to find all Models")
    public ResponseEntity<List<TSDModelDTO>> getTSDModelsConfigured() {
        var models = service.findAllTSDModelsWithConfiguration();

        return models == null || models.isEmpty()
                ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
                : new ResponseEntity<>(models, HttpStatus.OK);
    }

    @GetMapping("ml/{modelId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all models",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = MLConfigurationDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "no valid solution found",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = RestError.class
                                    )
                            )
                    )
            }
    )
    @Timed(value = "getModelSolution.time", description = "Time taken to find all Solutions that have been trained")
    public ResponseEntity<List<MLConfigurationDTO>> getValidSolutions(@PathVariable @NonNull Long modelId) {
        log.info("model id: {}", modelId);
        var configurations = service.findAllValidMlConfigurations(modelId);
        return configurations == null || configurations.isEmpty()
                ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
                : new ResponseEntity<>(configurations, HttpStatus.OK);
    }


    @GetMapping("tsd/{modelId}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all models",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = TSDConfigurationDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "models not found"
                    )
            }
    )
    @Timed(value = "getModelSolution.time", description = "Time taken to find all Solutions that have been trained")
    public ResponseEntity<List<TSDConfigurationDTO>> getValidTSDConfiguration(@PathVariable @NonNull Long modelId) {
        var configurations = service.findAllValidTSDConfigurations(modelId);
        return configurations == null || configurations.isEmpty()
                ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
                : new ResponseEntity<>(configurations, HttpStatus.OK);
    }

    @GetMapping("tsd/{modelId}/tsd_config/{configId}/trainData")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "found all models",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = TSDConfigurationDTO.class))
                            )
                    ),
                    @ApiResponse(
                            responseCode = "404",
                            description = "models not found"
                    )
            }
    )
    @Timed(value = "getModelSolution.time", description = "Time taken to find all Solutions that have been trained")
    public ResponseEntity<List<TrainDataDTO>> getTrainDataOfConfiguration(@PathVariable @NonNull Long modelId, @PathVariable @NonNull Long configId) {
        var data = service.findAllTrainDataSets(modelId, configId);
        return data == null || data.isEmpty()
                ? new ResponseEntity<>(HttpStatus.NOT_FOUND)
                : new ResponseEntity<>(data, HttpStatus.OK);
    }

}
