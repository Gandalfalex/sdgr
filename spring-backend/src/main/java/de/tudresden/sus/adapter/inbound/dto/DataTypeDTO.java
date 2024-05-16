package de.tudresden.sus.adapter.inbound.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.HashMap;
import java.util.Map;

@Data
@Accessors(chain = true)
public class DataTypeDTO {

    @JsonProperty("name")
    private String name;

    @JsonProperty("description")
    private String description;

    @JsonProperty("data_type")
    private DataTypes type;

    @JsonProperty("is_preview_visible")
    private boolean isPreviewVisible;

    @JsonProperty("schema")
    private Map<String, Object> schema = new HashMap<>();

    @JsonProperty("ui_schema")
    private Map<String, Object> uiSchema = new HashMap<>();

}
