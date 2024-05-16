package de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata;

import com.fasterxml.jackson.annotation.JsonProperty;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Accessors(chain = true)
public class MlDataSetDTO extends PlainDataDTO {

    @Schema(name = "dataType", nullable = false, description = "the dataType it represents")
    private final DataTypes dataType = DataTypes.ML;

    @Schema(name = "configurationId", nullable = false, description = "Configuration it belongs to")
    private Long configurationId;

    @Schema(name = "modelId", nullable = false, description = "the model it belongs to")
    private Long modelId;

    @JsonProperty("prediction_length")
    @Schema(name = "prediction_length", nullable = true, description = "the model it belongs to")
    private Integer predictionLength;

    @JsonProperty("start_value")
    @Schema(name = "start_value", nullable = true, description = "starting point of the prediction")
    private Integer startingPoint;

    @JsonProperty(value = "generation_option", defaultValue = "GENERATE")
    @Schema(name = "generation_option", nullable = false, description = "operation that should be performed when calling the django", defaultValue = "GENERATE")
    private Operation generationOption;

    @JsonProperty("predict")
    @Schema(name = "predict", nullable = true, description = "predictionAllowed")
    private boolean predict;

}
