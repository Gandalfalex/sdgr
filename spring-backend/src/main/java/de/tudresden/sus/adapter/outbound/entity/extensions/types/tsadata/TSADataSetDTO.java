package de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata;

import com.fasterxml.jackson.annotation.JsonProperty;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Accessors(chain = true)
public class TSADataSetDTO extends PlainDataDTO {

    @Schema(name = "dataType", nullable = false, description = "the dataType it represents")
    private final DataTypes dataType = DataTypes.TSA;

    @Schema(name = "configurationId", nullable = false, description = "the config it belongs to")
    private Long configurationId;

    @Schema(name = "modelId", nullable = false, description = "the model it belongs to")
    private Long modelId;

    @Schema(name = "configs")
    @JsonProperty("configs")
    private List<LevelConfigDTO> levelConfig = new ArrayList<>();
}
