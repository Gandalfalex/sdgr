package de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata;

import lombok.Getter;

@Getter
public enum Operation {
    FORECAST("forecast"),
    GENERATE("generate");

    private final String value;

    Operation(String value) {
        this.value = value;
    }
}
