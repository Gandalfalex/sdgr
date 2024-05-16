package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies.NoSeason;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.strategies.SineSeason;

public enum Seasons {

    NONE("None", NoSeason.class),
    SINE("Sine", SineSeason.class);

    private final String displayName;

    private final String type;

    private final Class<? extends Season> strategyClass;

    Seasons(String displayName, Class<? extends Season> strategyClass) {
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

    public Class<? extends Season> getStrategyClass() {
        return this.strategyClass;
    }

}
