package de.tudresden.sus.adapter.outbound.domain_objects;

import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.List;
import java.util.Optional;

@Data
@Accessors(chain = true)
public class DataSetDO {
    private String name;
    private Long id;
    private List<String> values;
    private float frequency;
    private int position;
    private DataTypes type;
    private int sleepTime;
}
