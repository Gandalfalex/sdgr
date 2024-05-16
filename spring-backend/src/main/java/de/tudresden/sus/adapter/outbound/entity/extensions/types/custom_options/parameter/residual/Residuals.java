package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.NoResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.PoissonResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.NormalResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.UniformResidual;

public enum Residuals {

    NONE("None", NoResidual.class),
    NORMAL("Normal", NormalResidual.class),
    UNIFORM("Uniform", UniformResidual.class),
    POISSON("Poisson", PoissonResidual.class);

    private final String displayName;

    private final String type;

    private final Class<? extends Residual> strategyClass;

    Residuals(String displayName, Class<? extends Residual> strategyClass) {
        this.displayName = displayName;
        this.type = strategyClass.getSimpleName();
        this.strategyClass = strategyClass;
    }

    public String getDisplayName() {
        return this.displayName;
    }

    public String getType() {
        return type;
    }

    public Class<? extends Residual> getStrategyClass() {
        return this.strategyClass;
    }
}
