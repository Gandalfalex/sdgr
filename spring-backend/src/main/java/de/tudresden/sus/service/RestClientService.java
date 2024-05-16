package de.tudresden.sus.service;

import de.tudresden.sus.adapter.outbound.restclient.models.dto.SignalDataDTO;
import de.tudresden.sus.adapter.outbound.restclient.models.dto.TrainDataConfigurationDTO;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.List;

@Service
public class RestClientService {

    public final RestClient restClient;
    @Value("${django.rest.base_url}")
    String BASE_URL;

    /**
     * This class represents a RestClientService.
     * It is responsible for creating a REST client with a base URL and default headers.
     */
    public RestClientService() {
        restClient = RestClient.builder()
                .baseUrl(BASE_URL)
                .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .build();
    }

    /**
     * Retrieves ML data from Django using the provided parameters.
     *
     * @param mId        The ID of the ML model.
     * @param cId        The ID of the configuration.
     * @param userToken  The user token for authorization.
     * @return The retrieved ML data as a SignalDataDTO object.
     */
    public SignalDataDTO getMLDataFromDjango(Long mId, Long cId, String userToken) {
        return restClient
                .post()
                .uri(BASE_URL + "/ml/ml_model/{mId}/ml_solution/{cId}/ml_configuration/load_data", mId, cId)
                .header("Authorization", "Bearer " + userToken)
                .contentType(MediaType.APPLICATION_JSON)
                .retrieve()
                .body(SignalDataDTO.class);
    }

    /**
     * Retrieves TSA data from Django using the provided parameters.
     *
     * @param mId        The ID of the TSA model.
     * @param cId        The ID of the configuration.
     * @param userToken  The user token for authorization.
     * @param data       The list of train data configurations.
     * @return The retrieved TSA data as a SignalDataDTO object.
     */
    public SignalDataDTO getTSADataFromDjango(Long mId, Long cId, String userToken, List<TrainDataConfigurationDTO> data) {
        return restClient
                .post()
                .uri(BASE_URL + "/tsd/tsd_model/{mId}/tsd_configuration/{cId}/configure", mId, cId)
                .header("Authorization", "Bearer " + userToken)
                .contentType(MediaType.APPLICATION_JSON)
                .body(data)
                .retrieve()
                .body(SignalDataDTO.class);
    }

    /**
     * Retrieves ML data forecast based on the provided parameters.
     *
     * @param mId        The ID of the ML model.
     * @param cId        The ID of the configuration.
     * @param userToken  The user token for authorization.
     * @param startPoint The starting point for the forecast.
     * @param length     The length of the forecast.
     * @return The ML data forecast as a SignalDataDTO object.
     */
    public SignalDataDTO getMLDataForecast(Long mId, Long cId, String userToken, String startPoint, String length){
        return restClient
                .post()
                .uri(BASE_URL + "/tsd/tsd_model/{mId}/tsd_configuration/{cId}/configure", mId, cId)
                .header("Authorization", "Bearer " + userToken)
                .body("starting_point: ")
                .contentType(MediaType.APPLICATION_JSON)
                .retrieve()
                .body(SignalDataDTO.class);
    }

    public void getRestClient() {
    }
}
