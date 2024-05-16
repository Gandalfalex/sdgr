package de.tudresden.sus.adapter.outbound.entity;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.schema.JSONSchema;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@NoArgsConstructor
@Entity(name = "DataType")
@Table(name = "data_type")
@Accessors(chain = true)
public class DataType {

    @Id
    @Column(name = "data_type_name")
    private String name;
    private String description;

    @Column(name = "data_type")
    private DataTypes type;

    @Column(name = "preview_showing")
    private boolean isPreviewVisible;

    @ManyToOne(fetch = FetchType.EAGER)
    private JSONSchema schema;
}
