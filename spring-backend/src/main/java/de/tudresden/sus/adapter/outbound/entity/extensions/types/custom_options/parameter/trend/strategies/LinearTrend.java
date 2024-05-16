package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.Trend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations.JsonFormProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class LinearTrend implements Trend {

    @JsonFormProperty(key = "description", text = "This is the slope (or multiplier) of the linear function.")
    private double slope;

    @JsonFormProperty(key = "description", text = "This is the offset (or y-intercept) of the linear function.")
    private double offset;

    @Override
    public double getValue(int time, boolean multiplicative) {
        return slope * time + offset;
    }
}
