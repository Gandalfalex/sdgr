package de.tudresden.sus.adapter.outbound.entity.extensions.types.schema;

import de.tudresden.sus.adapter.outbound.entity.extensions.DataTypeSchema;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.util.HashMap;
import java.util.Map;

@Data
@NoArgsConstructor
@Entity(name = "JSONSchema")
@Table(name = "json_schemas")
@Accessors(chain = true)
public class JSONSchema {

    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @Column(columnDefinition = "jsonb", name = "schema", nullable = true)
    @JdbcTypeCode( SqlTypes.JSON )
    private Map<String, Object> schema = new HashMap<>();

    @Column(columnDefinition = "jsonb", name = "ui_schema", nullable = true)
    @JdbcTypeCode( SqlTypes.JSON )
    private Map<String, Object> uiSchema = new HashMap<>();

    @Column(name = "schema_type")
    private DataTypeSchema schemaType;
}
