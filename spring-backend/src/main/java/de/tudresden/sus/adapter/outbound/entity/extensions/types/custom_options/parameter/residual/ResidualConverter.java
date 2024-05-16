package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Component;

import jakarta.persistence.AttributeConverter;

@Component
public class ResidualConverter implements AttributeConverter<Residual, String> {

    @Override
    public String convertToDatabaseColumn(Residual attribute) {
        try {
            return new ObjectMapper().writeValueAsString(attribute);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public Residual convertToEntityAttribute(String dbData) {
        try {
            return new ObjectMapper().readValue(dbData, Residual.class);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}