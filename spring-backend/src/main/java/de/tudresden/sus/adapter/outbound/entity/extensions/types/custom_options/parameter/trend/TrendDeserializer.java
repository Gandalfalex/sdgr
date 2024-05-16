package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.Trend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.CustomFormulaTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.LinearTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.NoTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.QuadraticTrend;
import lombok.extern.slf4j.Slf4j;

import java.io.IOException;

@Slf4j
public class TrendDeserializer extends JsonDeserializer<Trend> {

    @Override
    public Trend deserialize(JsonParser jp, DeserializationContext ctxt) throws IOException {
        ObjectMapper mapper = (ObjectMapper) jp.getCodec();
        JsonNode node = mapper.readTree(jp);
        log.info("{}", node);
        String trendType = node.get("type").asText();

        return switch (trendType) {
            case "LinearTrend" -> mapper.treeToValue(node, LinearTrend.class);
            case "QuadraticTrend" -> mapper.treeToValue(node, QuadraticTrend.class);
            case "CustomFormulaTrend" -> mapper.treeToValue(node, CustomFormulaTrend.class);
            case "NoTrend" -> mapper.treeToValue(node, NoTrend.class);
            default -> throw new IllegalArgumentException("Unknown trend type: " + trendType);
        };
    }
}