package de.tudresden.sus.adapter.inbound.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class LogMessageDTO {

    @Schema(name="message", description = "the send message")
    private String message;
    @Schema(name="time", description = "the time it was send")
    private String time;
    @Schema(name="sendSession", description = "the session it was send in")
    private String sendSession;
    @Schema(name="dataSetName", description = "the dataset that send the value")
    private String dataSetName;

    @Override
    public String toString(){
        return "LogMessageDTO[" +
                "message " + message +
                ", time " + time +
                ", sendSession " + sendSession +
                ", dataSetName " + dataSetName +
                "]";
    }
}
