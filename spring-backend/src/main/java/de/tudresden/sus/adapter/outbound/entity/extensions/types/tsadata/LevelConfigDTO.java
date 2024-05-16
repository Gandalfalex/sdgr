package de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.Map;

@Data
@Accessors(chain = true)
public class LevelConfigDTO {

    @Schema(name = "trainDataId", nullable = false, description = "id of train data")
    @JsonProperty("trainDataId")
    private Long trainDataId;

    @Schema(name = "level_config", nullable = true)
    @JsonProperty("level_configs")
    private Map<String, Object> levelConfig;
}
