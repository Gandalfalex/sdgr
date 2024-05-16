package de.tudresden.sus.adapter.inbound.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class RefreshTokenRequest {
    @JsonProperty("token")
    private String token;
}