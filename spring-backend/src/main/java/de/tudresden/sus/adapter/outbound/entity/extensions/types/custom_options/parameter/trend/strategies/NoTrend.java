package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.Trend;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class NoTrend implements Trend {

    @Override
    public double getValue(int time, boolean multiplicative) {
        return multiplicative ? 1 : 0;
    }

}
