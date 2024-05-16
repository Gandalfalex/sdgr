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
public class TSDConfigurationDTO {
    @JsonProperty("id")
    @Schema(description = "Unique identifier for the solution builder")
    private Long id;

    @JsonProperty("name")
    @Schema(description = "Name representation for the frontend")
    private String name;

    @JsonProperty("mlmodel_id")
    @Schema(description = "Associated model's unique identifier")
    private TSDModelDTO tsdModel;

    @JsonProperty("created_at")
    @Schema(description = "Creation timestamp of the solution builder")
    private Instant createdAt;

    @JsonProperty("max_length")
    @Schema(description = "Max size of elements this model can produce")
    private Integer maxLength;

    @JsonProperty("levelConfig")
    @Schema(description = "configs for each level")
    private String levelConfig;

}
