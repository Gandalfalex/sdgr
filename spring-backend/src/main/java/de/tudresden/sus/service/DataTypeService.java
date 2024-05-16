package de.tudresden.sus.service;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.inbound.dto.DataTypeDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.Operation;
import de.tudresden.sus.adapter.outbound.mapper.DataTypeMapper;
import de.tudresden.sus.adapter.outbound.repositories.DataTypeRepository;
import de.tudresden.sus.adapter.outbound.repositories.SchemaValidationFormRepository;
import de.tudresden.sus.adapter.outbound.restclient.models.repos.MLConfigurationRepository;
import de.tudresden.sus.ports.DataTypeServicePort;
import de.tudresden.sus.ports.StrategyServicePort;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;


@Service
@RequiredArgsConstructor
@Slf4j
public class DataTypeService implements DataTypeServicePort {

    private final DataTypeRepository repository;
    private final DataTypeMapper mapper;
    private final StrategyServicePort strategyService;
    private final SchemaValidationFormRepository validationFormRepository;
    private final MLConfigurationRepository configurationRepository;

    public List<DataTypeDTO> getAllDataTypes() {
        return repository.findAll().stream().map(mapper::toDTO).toList();
    }


    public DataTypeDTO save(DataTypeDTO entity) {
        var temp = repository.save(mapper.fromDTO(entity));
        return mapper.toDTO(temp);
    }

    public DataTypeDTO findByName(String name) {
        return repository.findById(name).map(mapper::toDTO).orElseThrow(() -> new EntityNotFoundException("datatype does not exist"));
    }

    public void deleteById(String name) {
        repository.deleteById(name);
    }


    public DataTypeDTO update(String name, DataTypeDTO entity) {
        if (repository.existsById(name)) {
            entity.setName(name);
            var temp = repository.save(mapper.fromDTO(entity));
            return mapper.toDTO(temp);
        } else {
            throw new EntityNotFoundException("No entity with name " + name + " found.");
        }
    }

    public DataTypeDTO buildCustomizeSchema(DataTypeDTO data) {
        var trendMap = new HashMap<String, JsonNode>();
        strategyService.getAllTrendStrategies().forEach(name -> {
            try {
                var someVal = name.get("type").toString().replaceAll("\"", "");
                trendMap.put(someVal, strategyService.getSchemaForTrend(someVal));
            } catch (Exception e) {
                log.error("no trend found");
            }
        });

        var seasonMap = new HashMap<String, JsonNode>();
        strategyService.getAllSeasonStrategies().forEach(name -> {
            try {
                var someVal = name.get("type").toString().replaceAll("\"", "");
                seasonMap.put(someVal, strategyService.getSchemaForSeason(someVal));
            } catch (Exception e) {
                log.error("no season found");
            }
        });


        var resMap = new HashMap<String, JsonNode>();
        strategyService.getAllResidualStrategies().forEach(name -> {
            try {
                var someVal = name.get("type").toString().replaceAll("\"", "");
                resMap.put(someVal, strategyService.getSchemaForResidual(someVal));
            } catch (Exception e) {
                log.error("no residual found");
            }
        });

        var ltes = strategyService.modifySchemaWithTrendOptions(data.getSchema(), trendMap, "trend");
        ltes = strategyService.modifySchemaWithTrendOptions(ltes, resMap, "residual");
        ltes = strategyService.modifySchemaWithTrendOptions(ltes, seasonMap, "season");

        strategyService.addNewElementWithClassNames(data.getUiSchema(), "trend", "inline-class");
        strategyService.addNewElementWithClassNames(data.getUiSchema(), "season", "inline-class");
        strategyService.addNewElementWithClassNames(data.getUiSchema(), "residual", "inline-class");

        data.setSchema(ltes);
        return data;
    }


    public DataTypeDTO buildMlModel(DataTypeDTO baseElement, Long configurationId) {
        if (configurationId == null) {
            return baseElement;
        }
        var config = configurationRepository.findById(configurationId).orElseThrow(() -> new EntityNotFoundException("config id not found"));
        return config.getMlmodel().isForcasting()
                ? extendSchema(baseElement, validationFormRepository
                .findFirstByName("forecasting_option").orElseThrow(() -> new EntityNotFoundException("validation schema does not exist")).getSchema())
                : removeGenerationOption(baseElement);
    }

    private DataTypeDTO removeGenerationOption(DataTypeDTO dto){
       var schema = dto.getSchema();
       Map<String, Object> propertiesMap = (Map<String, Object>) schema.get("properties");

        if (propertiesMap != null) {
            propertiesMap.remove("generation_option");
        }

        List<String> requiredList = (List<String>) schema.get("required");
        if (requiredList != null) {
            requiredList.remove("generation_option");
        }
        return dto;
    }

    public DataTypeDTO buildTSAModel(DataTypeDTO baseElement){
        log.info("called tsa- model");
        return extendSchema(baseElement, validationFormRepository.findFirstByName("forecasting_option").orElseThrow(() -> new EntityNotFoundException("validation schema does not exist")).getSchema());
    }

    private DataTypeDTO extendSchema(DataTypeDTO data, Map<String, Object> allOfPart) {
        Map<String, Object> extendedSchema = new HashMap<>(data.getSchema());

        // Add the 'allOf' property
        extendedSchema.put("allOf", allOfPart.get("allOf"));
        log.info("{}", allOfPart.get("allOf"));
        // Add the 'generation_option' property
        Map<String, Object> generationOption = new HashMap<>();
        generationOption.put("enum", Arrays.stream(Operation.values()).map(Enum::name).toList());
        generationOption.put("default", "GENERATE");
        generationOption.put("type", "string");

        Map<String, Object> properties = (Map<String, Object>) extendedSchema.getOrDefault("properties", new HashMap<>());
        properties.put("generation_option", generationOption);

        // Update the 'properties' in the extended schema
        extendedSchema.put("properties", properties);

        data.setSchema(extendedSchema);
        return data;
    }
}
