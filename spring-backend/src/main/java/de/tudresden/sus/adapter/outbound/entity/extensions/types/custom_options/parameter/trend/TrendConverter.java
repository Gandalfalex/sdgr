package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import jakarta.persistence.AttributeConverter;

@Component
public class TrendConverter implements AttributeConverter<Trend, String> {

    @Override
    public String convertToDatabaseColumn(Trend attribute) {
        try {
            return new ObjectMapper().writeValueAsString(attribute);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Trend convertToEntityAttribute(String dbData) {
        try {
            return new ObjectMapper().readValue(dbData, Trend.class);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}