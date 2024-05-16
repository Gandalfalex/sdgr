package de.tudresden.sus.adapter.outbound.domain_objects;

import lombok.Data;
import lombok.experimental.Accessors;

import java.util.List;

@Data
@Accessors(chain = true)
public class TrackDO {
    private Long id;
    private String name;
    private boolean isRepeating;
    private List<DataSetDO> datasets;
    private String unit;
}
