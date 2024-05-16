package de.tudresden.sus.ports;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public interface StrategyServicePort {
    List<JsonNode> getAllTrendStrategies();
    JsonNode getSchemaForTrend(String key);
    List<JsonNode> getAllSeasonStrategies();
    JsonNode getSchemaForSeason(String key);
    List<JsonNode> getAllResidualStrategies();
    JsonNode getSchemaForResidual(String key);
    Map<String, Object> modifySchemaWithTrendOptions(Map<String, Object> baseSchema, Map<String, JsonNode> options, String type);
    void addNewElementWithClassNames(Map<String, Object> uiSchema, String elementName, String classNames);
}
