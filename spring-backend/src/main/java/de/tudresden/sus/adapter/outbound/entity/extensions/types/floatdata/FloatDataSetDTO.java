package de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata;

import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.inbound.dto.PlainDataDTO;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.Residual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.ResidualDeserializer;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.Season;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.SeasonDeserializer;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.Trend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.TrendDeserializer;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.*;
import lombok.experimental.Accessors;

/**
 * Data transfer object representing a dataset when communicating via the API.
 */
@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Accessors(chain = true)
public class FloatDataSetDTO extends PlainDataDTO {

    @Schema(name = "calculationMethod", description = "use multiplicative or additive value calculation")
    private String calculationMethod;

    @Schema(name = "trendOption", nullable = false, description = "the increasing or decreasing value in the series, can also take a custom formula using x as time parameter")
    @JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
    @JsonDeserialize(using = TrendDeserializer.class)
    private Trend trendOption;

    @Schema(name = "seasonOption", nullable = false, description = "the repeating short-term cycle in the series")
    @JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
    @JsonDeserialize(using = SeasonDeserializer.class)
    private Season seasonOption;

    @Schema(name = "residualOption", nullable = false, description = "the random variation in the series")
    @JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
    @JsonDeserialize(using = ResidualDeserializer.class)
    private Residual residualOption;

    @Schema(name = "residual", nullable = false, description = "the random variation in the series, only the name")
    private String residual;
    @Schema(name = "trend", nullable = false, description = "the increasing or decreasing value in the series, can also take a custom formula using x as time parameter, only the name")
    private String trend;
    @Schema(name = "season", nullable = false, description = "the repeating short-term cycle in the series, only the name")
    private String season;

    @Schema(name = "dataType", nullable = false, description = "the dataType it represents")
    private final DataTypes dataType = DataTypes.FLOAT;
}
