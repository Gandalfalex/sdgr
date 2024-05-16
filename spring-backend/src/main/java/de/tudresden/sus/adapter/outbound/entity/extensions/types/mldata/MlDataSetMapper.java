package de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata;

import de.tudresden.sus.adapter.outbound.restclient.models.repos.MLConfigurationRepository;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
@Slf4j
public class MlDataSetMapper {

    private final MLConfigurationRepository repository;

    @SneakyThrows
    public MlDataSetDTO toDTO(MlDataSet eo) {
        return new MlDataSetDTO()
                .setConfigurationId(eo.getMlConfig().getMlConfiguration().getId())
                .setModelId(eo.getMlConfig().getMlConfiguration().getMlmodel().getId())
                .setPredict(eo.getMlConfig().getMlConfiguration().getMlmodel().isForcasting())
                .setGenerationOption(eo.getMlConfig().getGenerationOption())
                .setStartingPoint(eo.getMlConfig().getStartingPoint())
                .setPredictionLength(eo.getMlConfig().getPredictionLength());
    }

    public MlDataSet toEO(MlDataSetDTO dto) {
        return mergeDoToEo((MlDataSet) new MlDataSet().setId(dto.getId()), dto);
    }

    public MlDataSet mergeDoToEo(MlDataSet eo, MlDataSetDTO dto) {
        return eo
                .setMlConfig(new MlConfigData()
                        .setMlConfiguration(repository.findById(dto.getConfigurationId()).orElse(null))
                        .setStartingPoint(dto.getStartingPoint())
                        .setPredictionLength(dto.getPredictionLength())
                        .setGenerationOption(dto.getGenerationOption()))

                ;
    }
}
