package de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata;

import de.tudresden.sus.adapter.outbound.restclient.models.entity.TrainData;
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
@Entity
@Accessors(chain = true)
public class TsdLevelTrainData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(columnDefinition = "jsonb", name = "level_config", nullable = true)
    @JdbcTypeCode( SqlTypes.JSON )
    private Map<String, Object> levelConfig = new HashMap<>();

    @ManyToOne(fetch = FetchType.LAZY)
    private TrainData trainData;

    @Override
    public String toString() {
        return "TsdLevelTrainData{" +
                "id=" + id +
                ", levelConfig=" + levelConfig +
                ", trainData=" + trainData.getId() +
                '}';
    }
}
