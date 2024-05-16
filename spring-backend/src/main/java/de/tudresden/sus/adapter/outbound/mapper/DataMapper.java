package de.tudresden.sus.adapter.outbound.mapper;

import com.fasterxml.jackson.databind.ObjectMapper;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import de.tudresden.sus.adapter.inbound.errorhandler.DataConversionException;
import de.tudresden.sus.adapter.outbound.entity.DataType;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata.CharDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata.CharDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata.CharDataSetMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata.FileDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata.FileDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata.FileDataSetMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSetMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.intdata.IntegerDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.intdata.IntegerDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.intdata.IntegerDataSetMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSetMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper.SleepDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper.SleepDataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper.SleepDataSetMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSADataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSADataSetDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSADataSetMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.CustomValueConverter;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSetDTO;
import jakarta.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Function;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataMapper {

    private final CharDataSetMapper stringMapper;
    private final FloatDataSetMapper floatMapper;
    private final IntegerDataSetMapper intMapper;
    private final MlDataSetMapper mlMapper;
    private final TSADataSetMapper tsaMapper;
    private final CustomValueConverter customValueConverter;
    private final SleepDataSetMapper sleepMapper;
    private final ObjectMapper objectMapper;
    private final FileDataSetMapper fileDataSetMapper;


    private Map<DataTypes, Function<PlainData, PlainDataDTO>> toDTOMap;
    private Map<DataTypes, Function<PlainDataDTO, PlainData>> toEOMap;

    @PostConstruct
    public void init() {
        toDTOMap = new HashMap<>();
        toDTOMap.put(DataTypes.FLOAT, dataElement -> floatMapper.toDTO((FloatDataSet) dataElement));
        toDTOMap.put(DataTypes.CHAR, dataElement -> stringMapper.toDTO((CharDataSet) dataElement));
        toDTOMap.put(DataTypes.INTEGER, dataElement -> intMapper.toDTO((IntegerDataSet) dataElement));
        toDTOMap.put(DataTypes.ML, dataElement -> mlMapper.toDTO((MlDataSet) dataElement));
        toDTOMap.put(DataTypes.TSA, dataElement -> tsaMapper.toDTO((TSADataSet) dataElement));
        toDTOMap.put(DataTypes.SLEEP, dataElement -> sleepMapper.toDTO((SleepDataSet) dataElement));
        toDTOMap.put(DataTypes.FILETYPE, dataElement -> fileDataSetMapper.toDTO((FileDataSet) dataElement));

        toEOMap = new HashMap<>();
        toEOMap.put(DataTypes.FLOAT, dataElement -> floatMapper.toEO((FloatDataSetDTO) dataElement));
        toEOMap.put(DataTypes.CHAR, dataElement -> stringMapper.toEO((CharDataSetDTO) dataElement));
        toEOMap.put(DataTypes.INTEGER, dataElement -> intMapper.toEO((IntegerDataSetDTO) dataElement));
        toEOMap.put(DataTypes.ML, dataElement -> mlMapper.toEO((MlDataSetDTO) dataElement));
        toEOMap.put(DataTypes.TSA, dataElement -> tsaMapper.toEO((TSADataSetDTO) dataElement));
        toEOMap.put(DataTypes.SLEEP, dataElement -> sleepMapper.toEO((SleepDataSetDTO) dataElement));
        toEOMap.put(DataTypes.FILETYPE, dataElement -> fileDataSetMapper.toEO((FileDataSetDTO) dataElement));
    }

    @SneakyThrows
    public PlainDataDTO toDTO(PlainData data) {

        var dto = toDTOMap.get(data.getDataType()).apply(data);
        if (dto == null) {
            throw new DataConversionException("cannot convert dto: %s".formatted(data));
        }
        return dto.setId(data.getId())
                .setFrequency(data.getFrequency())
                .setName(data.getName())
                .setNumSamples(data.getNumSamples())
                .setCustomValues(data.getCustomValues() == null ? null : objectMapper.readTree(customValueConverter.convertToDatabaseColumn(data.getCustomValues())))
                .setPosition(data.getPosition());
    }

    public PlainData toEO(PlainDataDTO data) {
        var eo = toEOMap.get(data.getDataType()).apply(data);
        if (eo == null) {
            throw new DataConversionException("cannot convert dto: %s".formatted(data));
        }
        return eo.setId(data.getId())
                .setFrequency(data.getFrequency() == null ? null : data.getFrequency())
                .setName(data.getName())
                .setNumSamples(data.getNumSamples())
                .setCustomValues(data.getCustomValues() == null ? null : customValueConverter.convertToEntityAttribute(data.getCustomValues().toString()))
                .setPosition(data.getPosition());
    }
}
