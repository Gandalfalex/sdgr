package de.tudresden.sus.adapter.inbound.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata.CharDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata.FileDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.intdata.IntegerDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper.SleepDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSADataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSetDTO;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.*;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.Map;


@JsonTypeInfo(
        use = JsonTypeInfo.Id.NAME,
        include = JsonTypeInfo.As.PROPERTY,
        property = "type")
@JsonSubTypes({
        @JsonSubTypes.Type(value = CharDataSetDTO.class, name = "char"),
        @JsonSubTypes.Type(value = IntegerDataSetDTO.class, name = "integer"),
        @JsonSubTypes.Type(value = MlDataSetDTO.class, name = "ml"),
        @JsonSubTypes.Type(value = TSADataSetDTO.class, name = "tsa"),
        @JsonSubTypes.Type(value = FloatDataSetDTO.class, name = "float"),
        @JsonSubTypes.Type(value = SleepDataSetDTO.class, name = "sleep"),
        @JsonSubTypes.Type(value = FileDataSetDTO.class, name = "filetype")
})
@Data
@Accessors(chain = true)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class PlainDataDTO {

    @Schema(name = "id", nullable = true, minimum = "1")
    private Long id;

    @Schema(name = "name", nullable = false, description = "name to identify the dataSet")
    @JsonProperty("name")
    @NotNull
    @NotBlank(message = "name is mandatory")
    @Size(min = 3, max = 40, message = "name length should not be shorter than 3 and not longer than 40")
    private String name;

    @Schema(name = "numSamples", nullable = true, minimum = "1", description = "sample set")
    @JsonProperty("numSamples")
    @Positive(message = "number of samples has to be a positive number")
    private Integer numSamples;

    @Schema(name = "position", nullable = true, description = "position inside the track")
    @JsonProperty("position")
    @Positive(message = "cannot have a negative position")
    private Integer position;

    @Schema(name = "frequency", nullable = false, description = "repetitions per second")
    @JsonProperty("frequency")
    @Positive(message = "cannot use negative frequency")
    private Float frequency;

    @Schema(name = "dataType", nullable = false, description = "DataType saved in backend")
    @JsonProperty("dataType")
    @NotNull(message = "datatype is required for mapping")
    private DataTypes dataType;

    @Schema(name = "customValues", description = "custom values for calculation")
    @JsonProperty("customValues")
    private JsonNode customValues;
}
