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
public class TSDModelDTO {
    @JsonProperty("id")
    @Schema(description = "Unique identifier for the model")
    private Long id;

    @JsonProperty("name")
    @Schema(description = "Name representation for the frontend")
    private String name;

    @JsonProperty("description")
    @Schema(description = "Description of the model for the frontend")
    private String description;

    @JsonProperty("created_at")
    @Schema(description = "Creation timestamp of the model")
    private Instant createdAt;
}
