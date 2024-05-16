package de.tudresden.sus.adapter.inbound.rest;

import de.tudresden.sus.adapter.inbound.dto.DataTypeDTO;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.ports.DataTypeServicePort;
import de.tudresden.sus.service.DataTypeService;
import io.micrometer.core.annotation.Timed;
import io.swagger.v3.oas.annotations.media.ArraySchema;
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
@RequestMapping("/api/data_types")
@RequiredArgsConstructor
@Slf4j
public class DataTypeController {


    private final DataTypeServicePort dataTypeService;


    @GetMapping("/dataTypes")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "returned all dataTypes",
                            content = @Content(
                                    mediaType = "application/json",
                                    array = @ArraySchema(schema = @Schema(implementation = DataTypeDTO.class))
                            )
                    )
            }
    )
    @Timed(value = "getDatasets.time", description = "Time taken to return datasets")
    public ResponseEntity<List<DataTypeDTO>> getDataTypes() {
        return ResponseEntity.ok().body(dataTypeService.getAllDataTypes());
    }

    @PostMapping("/dataTypes")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "saved",
                            content = @Content(
                                    mediaType = "application/json",
                                    schema = @Schema(implementation = DataTypeDTO.class)
                            )
                    )
            }
    )
    @Timed(value = "getDatasets.time", description = "Time taken to return datasets")
    public ResponseEntity<DataTypeDTO> saveDataType(@RequestBody DataTypeDTO dataTypeDTO) {
        return ResponseEntity.ok().body(dataTypeService.save(dataTypeDTO));
    }

    @GetMapping("/dataTypes/{name}")
    @ApiResponses(
            value = {
                    @ApiResponse(
                            responseCode = "200",
                            description = "returned all dataTypes"
                    )
            }
    )
    @Timed(value = "getDatasets.time", description = "Time taken to return datasets")
    public ResponseEntity<DataTypeDTO> getDataTypeByName(@PathVariable String name, @RequestParam(required = false) Long configurationId) {
        var dto = dataTypeService.findByName(name.toUpperCase());

        var element = switch (DataTypes.valueOf(name.toUpperCase())) {
            case FLOAT, INTEGER -> dataTypeService.buildCustomizeSchema(dto);
            case ML -> dataTypeService.buildMlModel(dto, configurationId);
            case TSA -> dataTypeService.buildTSAModel(dto);
            default -> dto;
        };
        return ResponseEntity.ok().body(element);
    }

}
