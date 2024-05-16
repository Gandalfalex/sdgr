package de.tudresden.sus.adapter.outbound.restclient.models.entity;

import de.tudresden.sus.adapter.outbound.entity.User;
import jakarta.persistence.*;
import lombok.Data;
import lombok.experimental.Accessors;

import java.time.Instant;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "tsd_configuration")
@Data
@Accessors(chain = true)
public class TSDConfiguration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "tsd_model_id", nullable = false)
    private TSDModel tsdModel;

    @Column(length = 50, nullable = false, updatable = false)
    private String name;

    @Column(length = 500, nullable = true)
    private String description;

    @Temporal(TemporalType.TIMESTAMP)
    private Instant createdAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @OneToMany(mappedBy = "tsdConfiguration", fetch = FetchType.LAZY)
    private List<TsdConfigurationTrainData> tsdConfigurationTrainData = new ArrayList<>();
}
