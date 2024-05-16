package de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata;

import de.tudresden.sus.adapter.outbound.repositories.TSDConfigDataRepository;
import de.tudresden.sus.adapter.outbound.repositories.TsdLevelTrainDataRepository;
import de.tudresden.sus.adapter.outbound.restclient.models.repos.TSDConfigurationRepository;
import de.tudresden.sus.adapter.outbound.restclient.models.repos.TrainDataRepository;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;


@RequiredArgsConstructor
@Service
@Slf4j
public class TSADataSetMapper {

    private final TSDConfigurationRepository repository;
    private final TSDConfigDataRepository tsdRepository;
    private final TrainDataRepository trainDataRepository;
    private final TsdLevelTrainDataRepository levelConfigRepository;


    @SneakyThrows
    public TSADataSetDTO toDTO(TSADataSet eo) {
        var dataSet = new TSADataSetDTO()
                .setConfigurationId(eo.getTsdConfig().getConfiguration().getId())
                .setModelId(eo.getTsdConfig().getConfiguration().getTsdModel().getId());

        if (eo.getTsdConfig().getTrainData() != null) {
            eo.getTsdConfig().getTrainData().forEach(levelTrainData -> {
                        log.info("getLevelConfig: {}", levelTrainData.getLevelConfig());
                        if (levelTrainData.getLevelConfig() == null) {
                            var customValue = eo.getTsdConfig()
                                    .getTrainData().stream()
                                    .filter(conf -> conf.getTrainData().getId().equals(levelTrainData.getTrainData().getId())).findFirst().orElse(null);
                            log.info("adding: {}", customValue);
                            dataSet.getLevelConfig()
                                    .add(new LevelConfigDTO().setLevelConfig(customValue != null ? customValue.getLevelConfig() : null).setTrainDataId(levelTrainData.getTrainData().getId()));
                        } else {
                            log.info("using default: {}", levelTrainData);
                            dataSet.getLevelConfig().add(new LevelConfigDTO().setTrainDataId(levelTrainData.getTrainData().getId()).setLevelConfig(levelTrainData.getLevelConfig()));
                        }
                    }
            );
        } else {
            log.info("no config found");
        }
        return dataSet;
    }

    @Transactional
    public TSADataSet toEO(TSADataSetDTO dto) {
        return mergeDoToEo((TSADataSet) new TSADataSet().setId(dto.getId()), dto);
    }

    @Transactional()
    public TSADataSet mergeDoToEo(TSADataSet eo, TSADataSetDTO dto) {
        log.info("{}", dto);
        var tsdConfiguration = repository.findById(dto.getConfigurationId()).orElse(null);

        if (tsdConfiguration == null) {
            log.info("error finding configuration");
            return eo;
        }
        // if dto contains specific level configs -> it contains specific data
        if (dto.getLevelConfig() != null) {
            TSDConfigData tsdConfigData = eo.getTsdConfig() != null ? eo.getTsdConfig() : new TSDConfigData();

            // remove all old elements
            var ids = dto.getLevelConfig().stream().map(LevelConfigDTO::getTrainDataId).toList();
            var trainDataList = tsdConfigData.getTrainData();
            trainDataList.removeIf(trainData -> ids.contains(trainData.getTrainData().getId()));

            tsdConfigData.setTrainData(trainDataList);

            TSDConfigData configData = tsdConfigData;

            dto.getLevelConfig().forEach(levelConfigDTO -> {
                // check tsdConfiguration
                // if element in tsdConfiguration -> it can be saved here!
                //else do other stuff
                trainDataRepository.findById(levelConfigDTO.getTrainDataId())
                        .stream().findFirst().ifPresent(data -> {
                            var trainData = levelConfigRepository.saveAndFlush(new TsdLevelTrainData()
                                    .setTrainData(data)
                                    .setLevelConfig(levelConfigDTO.getLevelConfig()));
                            if (configData.getTrainData().stream().noneMatch(existingTrainData -> existingTrainData.getId().equals(data.getId()))) {
                                configData.getTrainData().add(trainData);
                            }
                        });
            });
            tsdConfigData.setConfiguration(tsdConfiguration);
            tsdConfigData = tsdRepository.save(tsdConfigData);
            eo.setTsdConfig(tsdConfigData);
        } else {
            log.info("setting default configuration");
            var temp = tsdRepository.save(new TSDConfigData().setConfiguration(tsdConfiguration));
            eo.setTsdConfig(temp);
        }
        return eo;
    }
}
