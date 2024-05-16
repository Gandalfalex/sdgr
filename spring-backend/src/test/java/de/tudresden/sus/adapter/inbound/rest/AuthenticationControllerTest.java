package de.tudresden.sus.adapter.inbound.rest;

import de.tudresden.sus.security.authentification.AuthenticationService;
import de.tudresden.sus.adapter.inbound.dto.JwtAuthenticationResponse;
import de.tudresden.sus.adapter.inbound.dto.SignUpRequest;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;

import static org.mockito.ArgumentMatchers.any;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
public class AuthenticationControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private AuthenticationService authenticationService;

    @Test
    public void testSignup() throws Exception{
        SignUpRequest signUpRequest = new SignUpRequest();
        signUpRequest.setFirstName("John");
        signUpRequest.setLastName("Doe");
        signUpRequest.setEmail("johndoe@example.com");
        signUpRequest.setPassword("password123");

        JwtAuthenticationResponse jwtAuthenticationResponse = new JwtAuthenticationResponse();
        Mockito.when(authenticationService.signup(any(SignUpRequest.class))).thenReturn(jwtAuthenticationResponse);

        mockMvc.perform(MockMvcRequestBuilders
                        .post("/api/v1/auth/signup")
                        .content("{\"firstName\":\"John\",\"lastName\":\"Doe\",\"email\":\"johndoe@example.com\",\"password\":\"password123\"}")
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk());

        Mockito.verify(authenticationService, Mockito.times(1)).signup(any(SignUpRequest.class));
    }
}