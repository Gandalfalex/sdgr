package de.tudresden.sus.security.authentification;

import de.tudresden.sus.adapter.inbound.dto.*;
import de.tudresden.sus.adapter.outbound.entity.RefreshToken;

public interface AuthenticationService {
    JwtAuthenticationResponse signup(SignUpRequest request);

    JwtAuthenticationResponse login(SigninRequest request);

    RefreshTokenResponse refresh(RefreshTokenRequest request);
}
