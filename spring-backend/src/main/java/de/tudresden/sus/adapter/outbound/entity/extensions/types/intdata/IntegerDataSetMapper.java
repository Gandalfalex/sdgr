package de.tudresden.sus.adapter.outbound.entity.extensions.types.intdata;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.CalculationMethod;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.TsdOption;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class IntegerDataSetMapper {

    @SneakyThrows
    public IntegerDataSetDTO toDTO(IntegerDataSet eo) {
        return new IntegerDataSetDTO()
                .setSeason(eo.getTsdOption().getSeason().getClass().getSimpleName())
                .setResidual(eo.getTsdOption().getResidual().getClass().getSimpleName())
                .setTrend(eo.getTsdOption().getTrend().getClass().getSimpleName())
                .setResidualOption(eo.getTsdOption().getResidual())
                .setSeasonOption(eo.getTsdOption().getSeason())
                .setTrendOption(eo.getTsdOption().getTrend())
                .setCalculationMethod(eo.getCalculationMethod().getValue());
    }

    @SneakyThrows
    public IntegerDataSet toEO(IntegerDataSetDTO dto) {
        var temp = (IntegerDataSet) new IntegerDataSet().setId(dto.getId());
        return mergeDoToEO(temp, dto);
    }

    public IntegerDataSet mergeDoToEO(IntegerDataSet eo, IntegerDataSetDTO dto) {
        var tsdOption = new TsdOption()
                .setResidual(dto.getResidualOption())
                .setSeason(dto.getSeasonOption())
                .setTrend(dto.getTrendOption());
        return eo
                .setTsdOption(tsdOption)
                .setCalculationMethod(CalculationMethod.of(dto.getCalculationMethod()));
    }
}
