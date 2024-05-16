package de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata;

import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Accessors(chain = true)
public class FileDataSetDTO extends PlainDataDTO {

    @Schema(name = "trainDataId", description = "Id of the traindata element")
    @NotNull
    private Long trainDataId;

    @Schema(name = "dataType", nullable = false, description = "the dataType it represents")
    private final DataTypes dataType = DataTypes.FILETYPE;
}
