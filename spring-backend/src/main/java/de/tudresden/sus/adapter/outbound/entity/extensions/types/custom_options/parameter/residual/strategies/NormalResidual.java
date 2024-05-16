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
public class NormalResidual extends Residual {

    @JsonFormProperty(key = "description", text = "The mean value of the normal distribution.")
    private double mean;

    @JsonFormProperty(key = "description", text = "The standard deviation of the normal distribution.")
    @JsonFormProperty(key = "minimum", value = 0)
    private double standardDeviation;

    @Override
    public double getValue(int time, boolean multiplicative, Random random) {
        return random.nextGaussian(mean, standardDeviation);
    }
}
