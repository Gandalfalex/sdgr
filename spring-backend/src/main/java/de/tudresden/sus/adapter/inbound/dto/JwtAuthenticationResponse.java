package de.tudresden.sus.adapter.inbound.dto;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class JwtAuthenticationResponse {
    private String token;
    private String refreshToken;
    private String refreshTokenTTL;
    private String languageCode;
}
