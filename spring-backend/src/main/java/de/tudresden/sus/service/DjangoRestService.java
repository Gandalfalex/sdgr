package de.tudresden.sus.service;

import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSet;
import de.tudresden.sus.adapter.outbound.repositories.UserRepository;
import de.tudresden.sus.adapter.outbound.restclient.DjangoRestClientURLBuilder;
import de.tudresden.sus.adapter.outbound.restclient.WebConfig;
import de.tudresden.sus.adapter.outbound.restclient.models.dto.*;
import de.tudresden.sus.adapter.outbound.restclient.models.repos.*;
import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import de.tudresden.sus.security.jwt.JwtService;
import jakarta.persistence.EntityNotFoundException;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.reactive.function.client.WebClient;

import java.net.URI;
import java.util.List;
import java.util.Objects;

@Service
@Slf4j
@RequiredArgsConstructor
public class DjangoRestService implements DjangoRestClientURLBuilder {


    private final WebClient restClient;
    @Value("${django.rest.base_url}")
    String BASE_URL;

    private final RestClientService restClientService;

    private final MLModelRepository mlModelRepo;
    private final MLSolutionBuilderRepository solutionRepo;
    private final MLConfigurationRepository configRepo;
    private final MLTrainingsInformationRepository trainingRepo;

    private final TSDConfigurationRepository tsdConfigurationRepository;
    private final TSDModelRepository tsdModelRepository;
    private final JwtService jwt;

    private final UserRepository userRepository;

    public List<String> callForMLData(Long modelId, Long configId, String user) {
        User sender = userRepository.findByEmail(user).orElseThrow(() -> new EntityNotFoundException("user could not be found"));
        String token = jwt.generateToken(sender);
        return restClientService.getMLDataFromDjango(modelId, configId, token).getData();
    }

    public List<String> callForMLForecast(MlDataSet dataSet, String user){
        User sender = userRepository.findByEmail(user).orElseThrow(() -> new EntityNotFoundException("user could not be found"));
        String token = jwt.generateToken(sender);
        return null;
    }


    public List<String> callForTSDData(Long modelId, Long configId, List<TrainDataConfigurationDTO> data, String user) {
        User sender = userRepository.findByEmail(user).orElseThrow(() -> new EntityNotFoundException("user could not be found"));
        String token = jwt.generateToken(sender);
        return restClientService.getTSADataFromDjango(modelId, configId, token, data).getData();
    }

    public List<MLModelsDTO> findAllMLModels() {
        return mlModelRepo.findAll().stream().map(m ->
                new MLModelsDTO().setId(m.getId()).setDescription(m.getDescription()).setCreatedAt(m.getCreatedAt()).setName(m.getName())
        ).toList();
    }

    public List<TSDModelDTO> findAllTSDModels() {
        return tsdModelRepository.findAll().stream().map(m ->
                new TSDModelDTO().setId(m.getId()).setDescription(m.getDescription()).setCreatedAt(m.getCreatedAt()).setName(m.getName())
        ).toList();
    }
    @AttachUser
    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public List<MLModelsDTO> findAllMLModelsWithConfiguration() {
        User user = UserAspect.getCurrentUser();
        return mlModelRepo.findMlModelByWithConfigurationByUserId(user.getId()).map(m ->
                new MLModelsDTO().setId(m.getId()).setDescription(m.getDescription()).setCreatedAt(m.getCreatedAt()).setName(m.getName())
        ).toList();
    }
    @AttachUser
    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public List<TSDModelDTO> findAllTSDModelsWithConfiguration() {
        User user = UserAspect.getCurrentUser();
        return tsdModelRepository.findTSDModelByWithConfigurationByUserId(user.getId()).map(m ->
                new TSDModelDTO().setId(m.getId()).setDescription(m.getDescription()).setCreatedAt(m.getCreatedAt()).setName(m.getName())
        ).toList();
    }

    /**
     * Finds all valid ML configurations for a given ML model.
     *
     * @param mlModelId the ID of the ML model
     * @return a list of MLConfigurationDTO containing the details of valid ML configurations
     * @throws EntityNotFoundException if the ML model with the given ID does not exist
     */
    public List<MLConfigurationDTO> findAllValidMlConfigurations(Long mlModelId) {
        var model = mlModelRepo.findById(mlModelId).orElseThrow(() -> new EntityNotFoundException("entity could not be found"));

        var configs = configRepo.findAllByMlmodel(model);
        log.info("found {} configs", configs);
        return configs.stream().map(configuration -> {
            var temp = solutionRepo.findByMlConfiguration(configuration).orElse(null);
            var information = trainingRepo.findMLTrainingInformationByMlSolution(temp).orElse(null);
            if (temp != null && information != null) {
                return new MLConfigurationDTO()
                        .setName(configuration.getName())
                        .setAccuracy(information.getAccuracy())
                        .setTrainingTime(information.getTrainingTime())
                        .setMaxLength(information.getMaxLength())
                        .setCreatedAt(information.getAddedTo())
                        .setTrainingIterations(information.getIterations())
                        .setId(configuration.getId());
            }
            log.info("could not find Configuration and TrainingInformation for model:{}", mlModelId);
            return null;
        }).filter(Objects::nonNull).toList();
    }

    /**
     * Finds all valid TSD configurations for a given TSD model ID.
     *
     * @param tsdModelId The ID of the TSD model
     * @return A list of TSDConfigurationDTO objects representing the valid TSD configurations
     * @throws EntityNotFoundException If the TSD model with the given ID does not exist
     */
    public List<TSDConfigurationDTO> findAllValidTSDConfigurations(Long tsdModelId) {
        var model = tsdModelRepository.findById(tsdModelId)
                .orElseThrow(() -> new EntityNotFoundException("tsd model could not be found"));
        var modelDTO = new TSDModelDTO()
                .setCreatedAt(model.getCreatedAt())
                .setName(model.getName())
                .setId(model.getId())
                .setDescription(model.getDescription());
        log.info("findAllValidTSDConfigurations");
        var configs = tsdConfigurationRepository.findAllByTsdModel(model);
        log.info("found {} configurations", configs.size());
        return configs.stream().map(config -> new TSDConfigurationDTO()
                .setTsdModel(modelDTO)
                .setName(config.getName())
                .setId(config.getId())
                .setCreatedAt(config.getCreatedAt())).toList();
    }


    public List<MLConfigurationDTO> findAllOccurrencesOfConfiguration(Long modelId, Long configId) {
        mlModelRepo.findById(modelId).orElseThrow(() -> new EntityNotFoundException("entity could not be found"));
        var config = configRepo.findById(configId).orElseThrow(() -> new EntityNotFoundException("entity could not be found"));
        return null;
    }


    public List<TrainDataDTO> findAllTrainDataSets(Long modelId, Long configId) {
        mlModelRepo.findById(modelId).orElseThrow(() -> new EntityNotFoundException("entity could not be found"));
        var config = tsdConfigurationRepository.findById(configId).orElseThrow(() -> new EntityNotFoundException("configuration could not be found"));
        return config != null && config.getTsdConfigurationTrainData() != null ?
                config.getTsdConfigurationTrainData().stream().map(data -> {
                    if (data != null)
                        return new TrainDataDTO()
                                .setId(data.getTrainData().getId())
                                .setName(data.getTrainData().getName());
                    else return new TrainDataDTO();
                }).toList()
                : List.of();
    }
}
