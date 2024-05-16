package de.tudresden.sus.adapter.inbound.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
public class PlainDataOccurrenceDTO {
    private Long projectId;
    private Long trackId;
    private Long dataSetId;
    private String projectName;
    private String trackName;
    private String dataSetName;
}
