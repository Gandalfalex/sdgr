package de.tudresden.sus.adapter.outbound.restclient.models.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.HashMap;
import java.util.Map;

@Data
@Accessors(chain = true)
public class TrainDataConfigurationDTO {

    @JsonProperty("trainDataId")
    private Long trainDataId;
    @JsonProperty("config")
    private Map<String, Object> config = new HashMap<>();
}
