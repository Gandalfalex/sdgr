package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.Residual;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

import java.util.Random;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class NoResidual extends Residual {

    @Override
    public double getValue(int time, boolean multiplicative, Random random) {
        return multiplicative ? 1 : 0;
    }
}
