package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies.NoSeason;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies.SineSeason;

import java.io.IOException;

public class SeasonDeserializer extends JsonDeserializer<Season> {

    @Override
    public Season deserialize(JsonParser jp, DeserializationContext ctxt) throws IOException {
        ObjectMapper mapper = (ObjectMapper) jp.getCodec();
        JsonNode node = mapper.readTree(jp);
        String trendType = node.get("type").asText();

        return switch (trendType) {
            case "NoSeason" -> mapper.treeToValue(node, NoSeason.class);
            case "SineSeason" -> mapper.treeToValue(node, SineSeason.class);
            default -> throw new IllegalArgumentException("Unknown trend type: " + trendType);
        };
    }
}
