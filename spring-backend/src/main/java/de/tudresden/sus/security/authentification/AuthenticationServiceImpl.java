package de.tudresden.sus.security.authentification;

import de.tudresden.sus.adapter.inbound.dto.*;
import de.tudresden.sus.adapter.inbound.errorhandler.InvalidCredentialException;
import de.tudresden.sus.adapter.outbound.entity.RefreshToken;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.repositories.RefreshTokenRepository;
import de.tudresden.sus.adapter.outbound.repositories.UserRepository;
import de.tudresden.sus.adapter.outbound.entity.UserRoles;
import de.tudresden.sus.security.jwt.JwtService;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Value;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.Optional;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthenticationServiceImpl implements AuthenticationService {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;
    private final RefreshTokenRepository refreshTokenRepository;

    @Value("${token.signing.refresh-ttl}")
    private Integer refreshTTL;

    @Override
    public JwtAuthenticationResponse signup(SignUpRequest request) {
        var user = User.builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail().toLowerCase())
                .password(passwordEncoder.encode(request.getPassword()))
                .role(UserRoles.USER).isSuperuser(false)
                .build();
        try {
            userRepository.save(user);
        } catch (Exception e) {
            log.info("user exists already");
            return null;
        }

        var jwt = jwtService.generateToken(user);


        return new JwtAuthenticationResponse().setToken(jwt);
    }

    @Override
    @SneakyThrows
    public JwtAuthenticationResponse login(SigninRequest request) {
        String email = request.getEmail().toLowerCase();
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(email, request.getPassword()));
        var user = userRepository.findByEmail(email)
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password."));
        var jwt = jwtService.generateToken(user);
        var refreshToken = createRefreshToken(user);

        return new JwtAuthenticationResponse()
                .setToken(jwt)
                .setRefreshToken(refreshToken.getToken())
                .setLanguageCode(user.getLanguageCode());
    }

    @Override
    public RefreshTokenResponse refresh(RefreshTokenRequest request) {
        var refreshToken = findByToken(request.getToken()).orElseThrow(() -> new InvalidCredentialException("refresh token not found"));
        verifyExpiration(refreshToken);
        String newJwt = jwtService.generateToken(refreshToken.getUserInfo());
        return new RefreshTokenResponse().setRefreshToken(refreshToken.getToken()).setToken(newJwt);
    }

    private RefreshToken createRefreshToken(User user) {
        RefreshToken token = refreshTokenRepository.findByUserInfo(user)
                .orElse(new RefreshToken()
                        .setUserInfo(userRepository.findByEmail(user.getEmail()).orElseThrow(() -> new InvalidCredentialException("user does not exist")))
                        .setToken(UUID.randomUUID().toString()));
        token.setExpiryDate(Instant.now().plusMillis(refreshTTL));
        return refreshTokenRepository.save(token);
    }

    private Optional<RefreshToken> findByToken(String token) {
        return refreshTokenRepository.findByToken(token);
    }

    private void verifyExpiration(RefreshToken token) {
        if (token.getExpiryDate().compareTo(Instant.now()) < 0) {
            refreshTokenRepository.delete(token);
            throw new InvalidCredentialException("refresh token does not exist");
        }
    }
}