package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.Season;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class NoSeason implements Season {

    @Override
    public double getValue(int time, boolean multiplicative) {
        return multiplicative ? 1 : 0;
    }
}
