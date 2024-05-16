package de.tudresden.sus.adapter.outbound.restclient.models.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;

import java.time.Instant;

@Getter
@Setter
@Accessors(chain = true)
public class MLConfigurationDTO {

    @JsonProperty("id")
    @Schema(description = "Unique identifier for the solution builder")
    private Long id;

    @JsonProperty("name")
    @Schema(description = "Name representation for the frontend")
    private String name;

    @JsonProperty("mlmodel")
    @Schema(description = "ml model")
    private MLModelsDTO mlModel;

    @JsonProperty("created_at")
    @Schema(description = "Creation timestamp of the solution builder")
    private Instant createdAt;

    @JsonProperty("training_time")
    @Schema(description = "Training time of the model")
    private Integer trainingTime;

    @JsonProperty("training_iterations")
    @Schema(description = "Training iterations of the model")
    private Integer trainingIterations;

    @JsonProperty("accuracy")
    @Schema(description = "Accuracy of the trained model")
    private Float accuracy;

    @JsonProperty("max_length")
    @Schema(description = "Max size of elements this model can produce")
    private Integer maxLength;
}
