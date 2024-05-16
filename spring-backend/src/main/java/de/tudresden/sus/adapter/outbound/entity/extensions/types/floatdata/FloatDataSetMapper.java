package de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.CalculationMethod;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.TsdOption;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
@Slf4j
public class FloatDataSetMapper {


    @SneakyThrows
    public FloatDataSetDTO toDTO(FloatDataSet eo) {
        return new FloatDataSetDTO()
                .setSeason(eo.getTsdOption().getSeason().getClass().getSimpleName())
                .setResidual(eo.getTsdOption().getResidual().getClass().getSimpleName())
                .setTrend(eo.getTsdOption().getTrend().getClass().getSimpleName())
                .setResidualOption(eo.getTsdOption().getResidual())
                .setSeasonOption(eo.getTsdOption().getSeason())
                .setTrendOption(eo.getTsdOption().getTrend())
                .setCalculationMethod(eo.getCalculationMethod().getValue());
    }

    @SneakyThrows
    public FloatDataSet toEO(FloatDataSetDTO dto) {
        var temp = (FloatDataSet) new FloatDataSet().setId(dto.getId());
        return mergeDoToEO(temp, dto);
    }

    public FloatDataSet mergeDoToEO(FloatDataSet eo, FloatDataSetDTO dto) {
        var tsdOption = new TsdOption()
                .setResidual(dto.getResidualOption())
                .setSeason(dto.getSeasonOption())
                .setTrend(dto.getTrendOption());
        return eo
                .setTsdOption(tsdOption)
                .setCalculationMethod(CalculationMethod.of(dto.getCalculationMethod()));
    }
}
