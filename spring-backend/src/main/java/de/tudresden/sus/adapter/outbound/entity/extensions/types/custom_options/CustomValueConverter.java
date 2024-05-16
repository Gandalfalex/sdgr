package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import jakarta.persistence.AttributeConverter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Converter class mapping custom values from map (backend) to list (frontend) and vice-versa.
 */
@Component
@Slf4j
public class CustomValueConverter implements AttributeConverter<Map<Integer, Double>, String> {

    @Override
    public String convertToDatabaseColumn(Map<Integer, Double> attribute) {
        var list = new ArrayList<CustomValue>();
        for (var entry : attribute.entrySet()) {
            list.add(new CustomValue(entry.getKey(), entry.getValue()));
        }

        try {
            return new ObjectMapper().writeValueAsString(list);
        } catch (JsonProcessingException e) {
            log.error("could not convert attributes, {}", e.getMessage());
            throw new RuntimeException(e);
        }
    }

    @Override
    public Map<Integer, Double> convertToEntityAttribute(String dbData) {
        var typeRef = new TypeReference<List<CustomValue>>() {};
        try {
            var list = new ObjectMapper().readValue(dbData, typeRef);
            var map = new HashMap<Integer, Double>();

            for (var entry : list) {
                map.put(entry.sampleNum(), entry.value());
            }

            return map;
        } catch (JsonProcessingException e) {
            log.error("could not convert custom values {}", e.getMessage());
            throw new RuntimeException(e);
        }
    }
}