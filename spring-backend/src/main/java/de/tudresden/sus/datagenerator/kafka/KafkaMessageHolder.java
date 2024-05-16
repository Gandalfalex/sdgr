package de.tudresden.sus.datagenerator.kafka;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@Data
@Accessors(chain = true)
public class KafkaMessageHolder {

    private Long trackId;
    private String trackName;
    private String unit;
    private String value;

}
