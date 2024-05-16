package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.NoResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.NormalResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.PoissonResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.UniformResidual;

import java.io.IOException;

public class ResidualDeserializer extends JsonDeserializer<Residual> {

    @Override
    public Residual deserialize(JsonParser jp, DeserializationContext ctxt) throws IOException {
        ObjectMapper mapper = (ObjectMapper) jp.getCodec();
        JsonNode node = mapper.readTree(jp);
        String trendType = node.get("type").asText();

        return switch (trendType) {
            case "NoResidual" -> mapper.treeToValue(node, NoResidual.class);
            case "NormalResidual" -> mapper.treeToValue(node, NormalResidual.class);
            case "PoissonResidual" -> mapper.treeToValue(node, PoissonResidual.class);
            case "UniformResidual" -> mapper.treeToValue(node, UniformResidual.class);
            default -> throw new IllegalArgumentException("Unknown trend type: " + trendType);
        };
    }
}

