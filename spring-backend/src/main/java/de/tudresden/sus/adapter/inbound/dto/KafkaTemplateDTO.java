package de.tudresden.sus.adapter.inbound.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class KafkaTemplateDTO {

    @JsonProperty("bootstrapServerAddress")
    private String bootstrapServers;
    @JsonProperty("topicId")
    private Long topicId;
    @JsonProperty("topic")
    private String topic;
    @JsonProperty("groupId")
    private String groupId;

}
