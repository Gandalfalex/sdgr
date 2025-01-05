package de.tudresden.sus.adapter.outbound.entity;


import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import de.tudresden.sus.adapter.outbound.entity.extensions.DataTypeOption;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata.CharDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata.FileDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata.FloatDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.intdata.IntegerDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata.MlDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper.SleepDataSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSADataSet;
import jakarta.persistence.*;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.Map;

@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@Accessors(chain = true)
@Data
@JsonTypeInfo(
        use = JsonTypeInfo.Id.NAME,
        include = JsonTypeInfo.As.PROPERTY,
        property = "type")
@JsonSubTypes({
        @JsonSubTypes.Type(value = CharDataSet.class, name = "char"),
        @JsonSubTypes.Type(value = FloatDataSet.class, name = "float"),
        @JsonSubTypes.Type(value = IntegerDataSet.class, name = "integer"),
        @JsonSubTypes.Type(value = MlDataSet.class, name = "ml"),
        @JsonSubTypes.Type(value = TSADataSet.class, name = "tsa"),
        @JsonSubTypes.Type(value = SleepDataSet.class, name = "sleep"),
        @JsonSubTypes.Type(value = FileDataSet.class, name = "filetype")
})
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public abstract class PlainData implements DataTypeOption {

    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @Column(name = "position")
    private Integer position;
    @Column(name = "numSamples")
    private Integer numSamples;
    @Column(name = "frequency")
    private Float frequency;
    @Column(name = "name")
    private String name;
    @Column(name = "dataType")
    private DataTypes dataType;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "data_set_custom_values",
            joinColumns = {@JoinColumn(name = "data_set_id", referencedColumnName = "id")})
    @MapKeyColumn(name = "sample_number")
    @Column(name = "custom_value")
    private Map<Integer, Double> customValues;
}
