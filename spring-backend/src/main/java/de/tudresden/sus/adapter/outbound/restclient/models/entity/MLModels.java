package de.tudresden.sus.adapter.outbound.restclient.models.entity;

import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.Immutable;

import java.time.Instant;

@Entity
@Table(name = "ml_model")
@Immutable
@Getter
public class MLModels {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 255, nullable = false, updatable = false)
    private String name;

    @Column(length = 255, nullable = false, updatable = false)
    private String description;

    @Temporal(TemporalType.TIMESTAMP)
    private Instant createdAt;

    @Column(name = "forcasting")
    private boolean forcasting;

}
