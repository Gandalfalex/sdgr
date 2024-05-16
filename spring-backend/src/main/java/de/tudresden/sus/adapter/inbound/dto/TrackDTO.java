package de.tudresden.sus.adapter.inbound.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

import java.util.List;

/**
 * Data transfer object representing a track when communicating via the API.
 */
@Data
public class TrackDTO {

    private Long id;

    @Schema(name = "repeating", description = "boolean, repeat the track or not")
    private boolean repeating;

    @JsonProperty(value = "name", required = true)
    @Schema(name = "name", description = "name of track")
    @NotNull
    @NotBlank(message = "name is mandatory")
    @Size(min = 3, max = 40, message = "name length should not be shorter than 3 and not longer than 40")
    private String name;

    @JsonProperty(value = "unit", required = true)
    @Schema(name = "unit", nullable = false, minimum = "1", description = "Unit")
    @NotNull
    @NotBlank(message = "unit is mandatory")
    @Size(min = 1, max = 20, message = "unit length should not longer than 20")
    private String unit;

    @Schema(name = "allowedDataTypes", nullable = true, description = "set a list of allowed DataTypes")
    private List<DataTypeDTO> allowedDataTypes;
}
