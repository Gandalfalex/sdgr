package de.tudresden.sus.adapter.outbound.restclient.models.entity;

import de.tudresden.sus.adapter.outbound.entity.User;
import jakarta.persistence.*;
import lombok.Data;
import lombok.experimental.Accessors;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.Instant;
import java.util.List;

@Entity
@Table(name = "train_data", schema = "public")
@Data
@Accessors(chain = true)
public class TrainData {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 50)
    private String name;

    @Column(columnDefinition = "jsonb", nullable = false, name = "time_series_value")
    @JdbcTypeCode( SqlTypes.JSON )
    private List<Float> values;

    @Temporal(TemporalType.TIMESTAMP)
    private Instant createdAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
