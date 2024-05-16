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
public class PoissonResidual extends Residual {

    @JsonFormProperty(key = "description", text = "The coefficient of variation for the poisson distribution.")
    @JsonFormProperty(key = "minimum", value = 0)
    private double lambda;

    @Override
    public double getValue(int time, boolean multiplicative, Random random) {
        var limit = Math.exp(-lambda);
        var rnd = random.nextDouble();
        int numSamples;

        for (numSamples = 0; rnd >= limit; numSamples++) {
            rnd *= random.nextDouble();
        }

        return numSamples;
    }
}
