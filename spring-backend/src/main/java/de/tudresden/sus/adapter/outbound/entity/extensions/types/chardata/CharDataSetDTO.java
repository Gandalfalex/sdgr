package de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata;

import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;

@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@Accessors(chain = true)
@Data
public class CharDataSetDTO extends PlainDataDTO {

    private List<String> alphabet = new ArrayList<>();

    private final DataTypes dataType = DataTypes.CHAR;
}
