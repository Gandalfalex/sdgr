package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.CustomFormulaTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.LinearTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.NoTrend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies.QuadraticTrend;

public enum Trends {

    NONE("None", NoTrend.class),
    LINEAR("Linear", LinearTrend.class),
    QUADRATIC("Quadratic", QuadraticTrend.class),
    FORMULA("Custom formula", CustomFormulaTrend.class);

    private final String displayName;

    private final String type;

    private final Class<? extends Trend> strategyClass;

    Trends(String displayName, Class<? extends Trend> strategyClass) {
        this.displayName = displayName;
        this.type = strategyClass.getSimpleName();
        this.strategyClass = strategyClass;
    }

    public String getDisplayName() {
        return displayName;
    }

    public String getType() {
        return this.type;
    }

    public Class<? extends Trend> getStrategyClass() {
        return this.strategyClass;
    }
}
