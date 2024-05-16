package de.tudresden.sus.adapter.inbound.rest;

import de.tudresden.sus.adapter.inbound.dto.RefreshTokenRequest;
import de.tudresden.sus.security.authentification.AuthenticationService;
import de.tudresden.sus.adapter.inbound.dto.JwtAuthenticationResponse;
import de.tudresden.sus.adapter.inbound.dto.SignUpRequest;
import de.tudresden.sus.adapter.inbound.dto.SigninRequest;
import de.tudresden.sus.adapter.inbound.dto.RefreshTokenResponse;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/auth")
@RequiredArgsConstructor
@Slf4j
@CrossOrigin
public class AuthenticationController {
    private final AuthenticationService authenticationService;
    @PostMapping("/signup")
    public ResponseEntity<JwtAuthenticationResponse> signup(@Valid @RequestBody SignUpRequest request) {
        log.info("{}", request);
        return ResponseEntity.ok(authenticationService.signup(request));
    }

    @PostMapping("/login")
    public ResponseEntity<JwtAuthenticationResponse> login(@Valid @RequestBody SigninRequest request) {
        log.info("{}", request);
        var response = authenticationService.login(request);
        log.info("token: {}", response);
        return  ResponseEntity.ok(response);
    }


    @PostMapping("/refresh")
    public ResponseEntity<RefreshTokenResponse> refresh(@Valid @RequestBody RefreshTokenRequest request){
        log.info("Refresh request: {}", request);
        var response = authenticationService.refresh(request);
        log.info("Refresh token: {}", response);
        return  ResponseEntity.ok(response);
    }
}