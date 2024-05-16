package de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata;

import de.tudresden.sus.adapter.outbound.restclient.models.entity.TSDConfiguration;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.*;

@Data
@NoArgsConstructor
@Entity
@Table
@Accessors(chain = true)
public class TSDConfigData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;


    @OneToMany(orphanRemoval = true, fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @Column(name = "train_data_configuration")
    private List<TsdLevelTrainData> trainData = new ArrayList<>();

    @ManyToOne
    @JoinColumn(name = "tsdConfig", nullable = false)
    private TSDConfiguration configuration;

    @Override
    public String toString() {
        return "TSDConfigData{" +
                "id=" + id +
                ", trainData size=" + trainData.size() +
                ", configuration=" + configuration.getId() +
                '}';
    }
}
