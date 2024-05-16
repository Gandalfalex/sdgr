package de.tudresden.sus.adapter.outbound.entity.extensions.types.schema;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.util.Map;


@Data
@NoArgsConstructor
@Entity(name = "SchemaValidationForm")
@Table(name = "schema_validation_forms")
@Accessors(chain = true)
public class SchemaValidationForms {

    @Id
    private Long id;
    @Column(name = "name")
    private String name;
    @Column(columnDefinition = "jsonb", name = "schema", nullable = true)
    @JdbcTypeCode( SqlTypes.JSON )
    private Map<String, Object> schema;
    @Column(columnDefinition = "jsonb", name = "ui_schema", nullable = true)
    @JdbcTypeCode( SqlTypes.JSON )
    private Map<String, Object> uiSchema;
}
