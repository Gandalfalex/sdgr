package de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper;

import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class SleepDataSetMapper {


    public SleepDataSetDTO toDTO(SleepDataSet eo) {
        return new SleepDataSetDTO()
                .setSleepTime(eo.getSleepTime());
    }

    public SleepDataSet toEO(SleepDataSetDTO dto) {
        return mergeDoToEo((SleepDataSet) new SleepDataSet().setId(dto.getId()), dto);
    }

    public SleepDataSet mergeDoToEo(SleepDataSet eo, SleepDataSetDTO dto) {
        return eo.setSleepTime(dto.getSleepTime());
    }
}
