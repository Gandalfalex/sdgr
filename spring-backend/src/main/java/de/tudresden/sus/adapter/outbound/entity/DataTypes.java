package de.tudresden.sus.adapter.outbound.entity;

import lombok.Getter;

@Getter
public enum DataTypes {

    CHAR("char"),
    FLOAT("float"),
    ML("ml"),
    TSA("tsa"),
    INTEGER ("integer"),
    SLEEP("sleep"),
    FILETYPE("filetype");

    private final String value;


    DataTypes(String value) {
        this.value = value;
    }
}
