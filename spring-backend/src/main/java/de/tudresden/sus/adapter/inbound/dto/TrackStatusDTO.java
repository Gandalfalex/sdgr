package de.tudresden.sus.adapter.inbound.dto;

import lombok.Data;
import lombok.experimental.Accessors;

import java.util.Objects;

@Data
@Accessors(chain = true)
public class TrackStatusDTO {
    private Long id;
    private String trackName;
    private String dataSetName;
    private float progress;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        TrackStatusDTO that = (TrackStatusDTO) o;
        return Objects.equals(trackName, that.trackName) && Objects.equals(id, that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(trackName, id);
    }
}
