package de.tudresden.sus.adapter.outbound.restclient.models.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.experimental.Accessors;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.util.HashMap;
import java.util.Map;

@Entity
@Table(name = "tsd_configuration_train_data")
@Data
@Accessors(chain = true)
public class TsdConfigurationTrainData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "jsonb", nullable = true)
    @JdbcTypeCode( SqlTypes.JSON )
    private Map<String, Object> levelConfig = new HashMap<>();

    @ManyToOne
    @JoinColumn(name = "train_data_id", nullable = false)
    private TrainData trainData;

    @ManyToOne
    private TSDConfiguration tsdConfiguration;

    @Override
    public String toString() {
        return "TsdConfigurationTrainData{" +
                "id=" + id +
                ", levelConfig=" + levelConfig +
                ", trainData=" + trainData.getId() +
                ", tsdConfiguration=" + tsdConfiguration.getId() +
                '}';
    }
}
