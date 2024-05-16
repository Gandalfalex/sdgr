package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.Season;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations.JsonFormProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class SineSeason implements Season {

    @JsonFormProperty(key = "description", text = "The frequency of the sine wave. It is the inverse of the period of the signal.")
    private double frequency;

    @JsonFormProperty(key = "description", text = "The phase (or shift along the x-axis) of the sine wave.")
    private double phase;

    @JsonFormProperty(key = "description", text = "The amplitude of the sine wave.")
    private double amplitude;

    @Override
    public double getValue(int time, boolean multiplicative) {
        return amplitude * Math.sin(frequency * (time + phase));
    }
}
