package de.tudresden.sus.adapter.outbound.restclient.models.entity;

import de.tudresden.sus.adapter.outbound.entity.User;
import lombok.Data;
import jakarta.persistence.*;

import java.time.Instant;

@Entity
@Table(name = "ml_configuration")
@Data
public class MLConfiguration {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 50, nullable = false, updatable = false)
    private String name;

    @Column(length = 500, nullable = true)
    private String description;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "ml_model_id", nullable = false)
    private MLModels mlmodel;

    @Temporal(TemporalType.TIMESTAMP)
    private Instant createdAt;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
}
