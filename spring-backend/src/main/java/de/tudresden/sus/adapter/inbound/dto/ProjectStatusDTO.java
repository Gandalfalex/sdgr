package de.tudresden.sus.adapter.inbound.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

@Data
@Accessors(chain = true)
@Slf4j
public class ProjectStatusDTO {

    @JsonProperty("id")
    private Long id;
    @JsonProperty("status")
    private String status;
    @JsonProperty("runningTracks")
    private CopyOnWriteArrayList<TrackStatusDTO> runningTracks = new CopyOnWriteArrayList<>();
    @JsonProperty("startTime")
    private String startTime;
    @JsonProperty("message")
    private String message;
    @JsonProperty("type")
    private String type = "spring";

    public synchronized void updateOrAdd(TrackStatusDTO dto){
        if (runningTracks == null){
            runningTracks = new CopyOnWriteArrayList<>();
        }
        if (runningTracks.contains(dto)){

            var id = runningTracks.indexOf(dto);
            runningTracks.get(id).setProgress(dto.getProgress()).setDataSetName(dto.getDataSetName());
        }
        else {
            runningTracks.add(dto);
        }
    }
}
