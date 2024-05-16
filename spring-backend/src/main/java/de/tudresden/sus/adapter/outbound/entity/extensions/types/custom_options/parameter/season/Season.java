package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies.NoSeason;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies.SineSeason;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME)
@JsonSubTypes({@JsonSubTypes.Type(NoSeason.class), @JsonSubTypes.Type(SineSeason.class)})
@JsonIgnoreProperties(ignoreUnknown = true)
public interface Season {
    double getValue(int time, boolean multiplicative);
}
