package de.tudresden.sus.service;

import de.tudresden.sus.adapter.outbound.restclient.models.dto.SignalDataDTO;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.context.jdbc.Sql;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriTemplate;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;

@SpringBootTest
@ActiveProfiles("test")
public class RestClientServiceTest {

    @Autowired
    private RestClientService restClientService;


    @Test
    public void testGetMLDataFromDjango() {
        // Arrange
        Long mId = 1L;
        Long cId = 1L;
        String userToken = "testToken";

        RestClient restClientMock = mock(RestClient.class, RETURNS_DEEP_STUBS);
        RestClientService restClientServiceSpy = spy(restClientService);

        doReturn(restClientMock).when(restClientServiceSpy).getRestClient();

        SignalDataDTO expectedResponse = new SignalDataDTO();
        when(restClientMock
                .post()
                .uri(new UriTemplate("/ml/ml_model/{mId}/ml_solution/{cId}/ml_configuration/load_data").expand(mId, cId))
                .header("Authorization", "Bearer " + userToken)
                .contentType(MediaType.APPLICATION_JSON)
                .retrieve()
                .body(SignalDataDTO.class)).thenReturn(expectedResponse);

        // Act
        SignalDataDTO actualResponse = restClientServiceSpy.getMLDataFromDjango(mId, cId, userToken);

        // Assert
        assertNotNull(actualResponse, "Response should not be null");
        verify(restClientMock.post()
                .uri(new UriTemplate("/ml/ml_model/{mId}/ml_solution/{cId}/ml_configuration/load_data").expand(mId, cId))
                .header("Authorization", "Bearer " + userToken)
                .contentType(MediaType.APPLICATION_JSON)
                .retrieve()).body(SignalDataDTO.class);

    }

}