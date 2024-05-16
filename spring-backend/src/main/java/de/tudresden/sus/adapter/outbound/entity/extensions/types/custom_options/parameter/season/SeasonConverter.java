package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import jakarta.persistence.AttributeConverter;

@Component
public class SeasonConverter implements AttributeConverter<Season, String> {

    @Override
    public String convertToDatabaseColumn(Season attribute) {
        try {
            return new ObjectMapper().writeValueAsString(attribute);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Season convertToEntityAttribute(String dbData) {
        try {
            return new ObjectMapper().readValue(dbData, Season.class);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}