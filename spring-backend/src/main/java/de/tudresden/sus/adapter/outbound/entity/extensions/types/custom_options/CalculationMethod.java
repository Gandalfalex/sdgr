package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options;

import java.util.Arrays;
import java.util.Objects;

/**
 * Calculation method that shall be used to compose trend, season and residuals in the dataset.
 */
public enum CalculationMethod {

    ADDITIVE("additive"),
    MULTIPLICATIVE("multiplicative");

    private final String value;

    CalculationMethod(String value) {
        this.value = value;
    }

    public String getValue() {
        return this.value;
    }

    public static CalculationMethod of(String value) {
        return Arrays.stream(values()).filter(c -> Objects.equals(c.getValue(), value)).findFirst().orElseThrow(IllegalArgumentException::new);
    }

}
