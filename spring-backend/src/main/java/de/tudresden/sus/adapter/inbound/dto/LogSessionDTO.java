package de.tudresden.sus.adapter.inbound.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class LogSessionDTO {
    @Schema(name="session", description = "the session in which messages where send")
    public String session;
}
