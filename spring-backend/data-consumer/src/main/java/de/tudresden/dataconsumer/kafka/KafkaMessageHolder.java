package de.tudresden.dataconsumer.kafka;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class KafkaMessageHolder {

    @JsonProperty("trackId")
    private Long trackId;
    @JsonProperty("unit")
    private String unit;
    @JsonProperty("value")
    private String value;
    @JsonProperty("trackName")
    private String trackName;

    @Override
    public String toString(){
        return "KafkaMessageHolder[" +
                "track_id: " + trackId +
                ", track_name: " + trackName +
                ", value: " + value +
                ", unit: " + unit +
                "]";
    }
}