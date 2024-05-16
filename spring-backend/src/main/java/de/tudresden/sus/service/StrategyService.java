package de.tudresden.sus.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations.JsonFormProperty;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.Residuals;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.Seasons;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.Trends;
import de.tudresden.sus.ports.StrategyServicePort;
import jakarta.persistence.EntityNotFoundException;
import org.springframework.stereotype.Component;

import java.lang.reflect.Field;
import java.util.*;

@Component
public class StrategyService implements StrategyServicePort {

    private static final ObjectMapper objectMapper = new ObjectMapper();

    /**
     * Returns all available trend strategies (linear, quadratic, ...)
     *
     * @return the list of trends
     */
    public List<JsonNode> getAllTrendStrategies() {
        var trends = Trends.values();

        return Arrays.stream(trends).map(trend -> {
            var node = JsonNodeFactory.instance.objectNode();
            node.put("type", trend.getType());
            node.put("displayName", trend.getDisplayName());
            return (JsonNode) node;
        }).toList();
    }

    /**
     * Returns the schema used for the JsonForms library for the given trend.
     *
     * @param key the given trend key (strategy).
     * @return the JsonSchema
     */
    public JsonNode getSchemaForTrend(String key) {
        // map key to trend
        var optTrend = Arrays.stream(Trends.values()).filter(t -> Objects.equals(t.getType(), key)).findFirst();

        // null if no match is found - returns 404 via REST
        if (optTrend.isEmpty()) {
            return null;
        }

        var trendClass = optTrend.get().getStrategyClass();
        return buildSchemaForClass(trendClass, false);
    }

    /**
     * Returns all available season strategies (sine, ...)
     *
     * @return the list of seasons
     */
    public List<JsonNode> getAllSeasonStrategies() {
        var seasons = Seasons.values();

        return Arrays.stream(seasons).map(season -> {
            var node = JsonNodeFactory.instance.objectNode();
            node.put("type", season.getType());
            node.put("displayName", season.getDisplayName());
            return (JsonNode) node;
        }).toList();
    }

    /**
     * Returns the schema used for the JsonForms library for the given season.
     *
     * @param key the given season type (strategy).
     * @return the JsonSchema
     */
    public JsonNode getSchemaForSeason(String key) {
        // map key to season
        var optSeason = Arrays.stream(Seasons.values()).filter(t -> Objects.equals(t.getType(), key)).findFirst();

        // null if no match is found - returns 404 via REST
        if (optSeason.isEmpty()) {
            return null;
        }

        var seasonClass = optSeason.get().getStrategyClass();
        return buildSchemaForClass(seasonClass, false);
    }

    /**
     * Returns all available residual strategies (uniform, normal, poisson, ...)
     *
     * @return the list of residuals
     */
    public List<JsonNode> getAllResidualStrategies() {
        var residuals = Residuals.values();

        return Arrays.stream(residuals).map(residual -> {
            var node = JsonNodeFactory.instance.objectNode();
            node.put("type", residual.getType());
            node.put("displayName", residual.getDisplayName());
            return (JsonNode) node;
        }).toList();
    }

    /**
     * Returns the schema used for the JsonForms library for the given residual.
     *
     * @param key the given residual type (strategy).
     * @return the JsonSchema
     */
    public JsonNode getSchemaForResidual(String key) {
        // map key to residual
        var optResidual = Arrays.stream(Residuals.values()).filter(t -> Objects.equals(t.getType(), key)).findFirst();

        // null if no match is found - returns 404 via REST
        if (optResidual.isEmpty()) {
            throw new EntityNotFoundException();
        }

        var residual = optResidual.get();

        var residualClass = residual.getStrategyClass();
        var includeSuperclass = residual != Residuals.NONE;
        return buildSchemaForClass(residualClass, includeSuperclass);
    }

    /**
     * Parses the attributes and annotations of the given class in a schema that is understood by JsonForms.
     *
     * @param clazz the class
     * @return the corresponding JsonForms schema
     */
    private JsonNode buildSchemaForClass(Class<?> clazz, boolean includeSuperclass) {
        var node = JsonNodeFactory.instance.objectNode();

        var fields = new ArrayList<>(Arrays.asList(clazz.getDeclaredFields()));
        if (includeSuperclass && clazz.getSuperclass() != null) {
            fields.addAll(Arrays.asList(clazz.getSuperclass().getDeclaredFields()));
        }

        // convert class attributes to properties with constraints
        var properties = JsonNodeFactory.instance.objectNode();
        for (Field field : fields) {
            var property = JsonNodeFactory.instance.objectNode();

            // add type information for property
            var type = mapToJsonType(field.getType());
            property.put("type", type);

            // add properties from annotations
            var annotations = field.getAnnotationsByType(JsonFormProperty.class);
            for (var annotation : annotations) {
                // if there is text, use text - otherwise use int value
                if (!annotation.text().isEmpty()) {
                    property.put(annotation.key(), annotation.text());
                } else {
                    property.put(annotation.key(), annotation.value());
                }
            }

            properties.set(field.getName(), property);
        }

        node.set("properties", properties);

        return node;
    }

    /**
     * Maps the Java Class of an attribute type to the corresponding type for JsonForms.
     *
     * @param type the type class.
     * @return the corresponding JsonForms type
     */
    private String mapToJsonType(Class<?> type) {
        return switch (type.getSimpleName()) {
            case "int", "long" -> "integer";
            case "String" -> "string";
            case "double" -> "number";
            default -> throw new IllegalStateException("unknown type for mapping: " + type.getSimpleName());
        };
    }

    public Map<String, Object> modifySchemaWithTrendOptions(
            Map<String, Object> baseSchema,
            Map<String, JsonNode> trendOptions,
            String type) {

        var capitalizedType = type.substring(0, 1).toUpperCase() + type.substring(1);
        Map<String, Object> properties = (Map<String, Object>) baseSchema.getOrDefault("properties", new HashMap<>());
        Map<String, Object> dependencies = (Map<String, Object>) baseSchema.getOrDefault("dependencies", new HashMap<>());

        Map<String, Object> trendProperty = new HashMap<>();
        trendProperty.put("type", "string");
        trendProperty.put("enum", new ArrayList<>(trendOptions.keySet()));
        trendProperty.put("default", "No" + capitalizedType);
        properties.put(type, trendProperty);

        Map<String, Object> trendDependencies = new HashMap<>();
        trendDependencies.put("oneOf", createTrendDependencyArray(trendOptions, type));
        dependencies.put(type, trendDependencies);

        baseSchema.put("properties", properties);
        baseSchema.put("dependencies", dependencies);
        return baseSchema;
    }

    private List<Map<String, Object>> createTrendDependencyArray(Map<String, JsonNode> options, String type) {
        List<Map<String, Object>> dependencyArray = new ArrayList<>();

        for (Map.Entry<String, JsonNode> entry : options.entrySet()) {
            Map<String, Object> conditionNode = new HashMap<>();
            Map<String, Object> ifCondition = new HashMap<>();

            ifCondition.put("properties", Map.of(type, Map.of("const", entry.getKey())));
            conditionNode.put("if", ifCondition);

            conditionNode.put("required", List.of(type));
            conditionNode.put("properties", Map.of(type, Map.of("const", entry.getKey())));

            // THEN part
            Map<String, Object> thenProperties = new HashMap<>();
            thenProperties.put(type + "Option", objectMapper.convertValue(entry.getValue(), Map.class));
            conditionNode.put("then", Map.of("properties", thenProperties, "required", getRequiredFields(entry.getValue())));

            dependencyArray.add(conditionNode);
        }

        return dependencyArray;
    }

    private List<String> getRequiredFields(JsonNode jsonNode) {
        if (jsonNode.has("required") && jsonNode.get("required").isArray()) {
            return objectMapper.convertValue(jsonNode.get("required"), List.class);
        }
        return new ArrayList<>();
    }

    public void addNewElementWithClassNames(Map<String, Object> uiSchema, String elementName, String classNames) {
        Map<String, Object> elementMap = new HashMap<>();
        elementMap.put("ui:classNames", classNames);
        uiSchema.put(elementName, elementMap);
    }
}
