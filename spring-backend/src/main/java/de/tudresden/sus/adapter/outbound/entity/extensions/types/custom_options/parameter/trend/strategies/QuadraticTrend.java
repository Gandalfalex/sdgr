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
public class QuadraticTrend implements Trend {

    @JsonFormProperty(key = "description", text = "The coefficient in the quadratic term in standard form.")
    private double a;

    @JsonFormProperty(key = "description", text = "The coefficient in the linear term in standard form.")
    private double b;

    @JsonFormProperty(key = "description", text = "The constant term in standard form.")
    private double c;

    @Override
    public double getValue(int time, boolean multiplicative) {
        return a * time * time + b * time + c;
    }
}
