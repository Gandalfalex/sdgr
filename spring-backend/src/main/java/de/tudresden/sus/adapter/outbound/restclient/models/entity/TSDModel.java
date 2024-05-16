package de.tudresden.sus.adapter.outbound.restclient.models.entity;

import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.Immutable;

import java.time.Instant;

@Entity
@Table(name = "tsd_models")
@Immutable
@Getter
public class TSDModel {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(length = 255, nullable = false, updatable = false)
    private String name;

    @Column(length = 255, nullable = false, updatable = false)
    private String description;

    @Temporal(TemporalType.TIMESTAMP)
    private Instant createdAt;
}
