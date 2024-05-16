package de.tudresden.sus.adapter.outbound.entity.extensions;

public enum DataTypeSchema {
    NUMERIC(0L),
    ALPHABETIC(1L),
    ML(2L),
    TSA(3L),
    SLEEP(4L),
    FILETYPE(5L);

    private final Long schemaId;

    DataTypeSchema(Long schemaId) {
        this.schemaId = schemaId;
    }

    public Long getSchemaId() {
        return schemaId;
    }
}
