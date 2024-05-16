package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.CustomFormulaTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.LinearTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.NoTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.QuadraticTrend;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME)
@JsonSubTypes({@JsonSubTypes.Type(NoTrend.class), @JsonSubTypes.Type(LinearTrend.class), @JsonSubTypes.Type(QuadraticTrend.class), @JsonSubTypes.Type(CustomFormulaTrend.class)})
@JsonIgnoreProperties(ignoreUnknown = true)
public interface Trend {
    double getValue(int time, boolean multiplicative);
}
