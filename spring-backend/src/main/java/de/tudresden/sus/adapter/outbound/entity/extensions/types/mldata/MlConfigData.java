package de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata;

import com.fasterxml.jackson.annotation.JsonEnumDefaultValue;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLConfiguration;
import jakarta.persistence.*;
import lombok.Data;
import lombok.experimental.Accessors;

@Entity(name = "MlConfigData")
@Table(name = "ml_config_data")
@Data
@Accessors(chain = true)
public class MlConfigData {

    @Id
    @Column
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    @ManyToOne(fetch = FetchType.EAGER)
    private MLConfiguration mlConfiguration;

    @Column(name = "prediction_length")
    private Integer predictionLength;
    @Column(name = "starting_point")
    private Integer startingPoint;
    @Column(name = "generation_option", nullable = false)
    private Operation generationOption;
}
