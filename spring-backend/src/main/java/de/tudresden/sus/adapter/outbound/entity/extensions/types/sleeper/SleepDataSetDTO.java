package de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper;

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
public class SleepDataSetDTO extends PlainDataDTO {

    @Schema(name = "sleepTime", nullable = false, description = "the time the process will stand still")
    @JsonProperty("sleepTime")
    private int sleepTime;

    @Schema(name = "dataType", nullable = false, description = "the dataType it represents")
    private final DataTypes dataType = DataTypes.SLEEP;
}
