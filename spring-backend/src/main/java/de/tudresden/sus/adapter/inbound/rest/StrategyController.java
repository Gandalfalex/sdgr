package de.tudresden.sus.adapter.inbound.rest;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.outbound.repositories.JSONSchemaRepository;
import de.tudresden.sus.ports.StrategyServicePort;
import de.tudresden.sus.security.authentification.RestError;
import de.tudresden.sus.service.StrategyService;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/strategies")
@CrossOrigin
@RequiredArgsConstructor
@Slf4j
public class StrategyController {

    private final StrategyServicePort strategyService;


    @GetMapping("/trend")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return a list of all trend types",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = JsonNode.class)
                            )
                    )
            }
    )
    public List<JsonNode> getAllTrendStrategies() {
        return strategyService.getAllTrendStrategies();
    }

    @GetMapping("/trend/{type}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return specific trend schema based on type",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = JsonNode.class)
                            )
                    )
            }
    )
    public ResponseEntity<JsonNode> getTrend(@PathVariable String type) {
        var schema = strategyService.getSchemaForTrend(type);
        if (schema == null) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(schema);
    }

    @GetMapping("/season")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return a list of all season types",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = JsonNode.class)
                            )
                    )
            }
    )
    public List<JsonNode> getAllSeasonStrategies() {
        return strategyService.getAllSeasonStrategies();
    }

    @GetMapping("/season/{type}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return season schema based on type",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = JsonNode.class)
                            )
                    )
            }
    )
    public ResponseEntity<JsonNode> getSeason(@PathVariable String type) {
        var schema = strategyService.getSchemaForSeason(type);
        if (schema == null) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(schema);
    }

    @GetMapping("/residual")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return a list of all residual types",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = JsonNode.class)
                            )
                    )
            }
    )
    public List<JsonNode> getAllResidualStrategies() {
        return strategyService.getAllResidualStrategies();
    }

    @GetMapping("/residual/{type}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "return residual schema based on type",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = JsonNode.class)
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
    public ResponseEntity<JsonNode> getResidual(@PathVariable String type) {
        var schema = strategyService.getSchemaForResidual(type);
        if (schema == null) {
            return ResponseEntity.notFound().build();
        }

        return ResponseEntity.ok(schema);
    }
}
