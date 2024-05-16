package de.tudresden.sus.adapter.outbound.restclient.models.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class TrainDataDTO {
    @JsonProperty("id")
    @Schema(name = "id", description = "Name representation for the frontend")
    private Long id;
    @JsonProperty("name")
    @Schema(name = "name", description = "Name representation for the frontend")
    private String name;
}
