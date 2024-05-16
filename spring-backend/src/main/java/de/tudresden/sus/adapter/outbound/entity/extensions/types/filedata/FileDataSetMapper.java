package de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata;

import de.tudresden.sus.adapter.outbound.restclient.models.repos.TrainDataRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;


@RequiredArgsConstructor
@Service
@Slf4j
public class FileDataSetMapper {

    private final TrainDataRepository trainDataRepository;

    @SneakyThrows
    public FileDataSetDTO toDTO(FileDataSet eo) {
        return new FileDataSetDTO()
                .setTrainDataId(eo.getTrainData().getId());
    }

    @SneakyThrows
    public FileDataSet toEO(FileDataSetDTO dto) {
        var temp = (FileDataSet) new FileDataSet().setId(dto.getId());
        return mergeDoToEO(temp, dto);
    }

    public FileDataSet mergeDoToEO(FileDataSet eo, FileDataSetDTO dto) {
        var traindata = trainDataRepository.findById(dto.getTrainDataId())
                .orElseThrow(() -> new EntityNotFoundException("TrainData does not exists"));
        return eo
                .setTrainData(traindata);
    }
}
