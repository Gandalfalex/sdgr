package de.tudresden.sus.adapter.inbound.websocket;

import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.repositories.UserRepository;
import de.tudresden.sus.service.JwtServiceImpl;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.util.MultiValueMap;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.server.support.DefaultHandshakeHandler;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;
import java.security.Principal;
import java.util.List;
import java.util.Map;

@Configuration
@Slf4j
public class WebSocketJWTHandshakeHandler extends DefaultHandshakeHandler {

    @Autowired
    JwtServiceImpl service;
    @Autowired
    UserRepository repository;

    @Override
    protected Principal determineUser(ServerHttpRequest request, WebSocketHandler wsHandler, Map<String, Object> attributes) {
        // Extract query parameters
        String jwtToken = extractTokenFromRequest(request);
        if (jwtToken != null) {
            User user = repository.findByEmail(service.extractUserName(jwtToken)).orElse(null);
            if (user != null) {
                log.info("user: {}", user);
                attributes.put("user", user.getEmail());
            }
        }
        return super.determineUser(request, wsHandler, attributes);
    }

    private String extractTokenFromRequest(ServerHttpRequest request) {
        URI uri = request.getURI();
        MultiValueMap<String, String> queryParams = UriComponentsBuilder.fromUri(uri).build().getQueryParams();
        List<String> tokenList = queryParams.get("token");
        if (tokenList != null && !tokenList.isEmpty()) {
            return tokenList.get(0);
        }
        return null;
    }
}