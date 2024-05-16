package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.Residual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations.JsonFormProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

import java.util.Random;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class UniformResidual extends Residual {

    @JsonFormProperty(key = "description", text = "The minimum value for the uniform distribution.")
    private double min;

    @JsonFormProperty(key = "description", text = "The maximum value for the uniform distribution.")
    private double max;

    @Override
    public double getValue(int time, boolean multiplicative, Random random) {
        return min + (max - min) * random.nextDouble();
    }
}
