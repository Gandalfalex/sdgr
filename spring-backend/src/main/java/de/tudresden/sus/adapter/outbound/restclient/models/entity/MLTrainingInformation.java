package de.tudresden.sus.adapter.outbound.restclient.models.entity;

import jakarta.persistence.*;
import lombok.Data;

import java.time.Instant;

@Data
@Entity
@Table(name = "ml_training_information")
public class MLTrainingInformation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name="ml_solution_id", nullable=false)
    private MLSolution mlSolution;

    @Temporal(TemporalType.TIMESTAMP)
    private Instant addedTo;

    private Integer trainingTime;

    private Integer iterations;

    private Integer targetIterations;

    private Integer targetAccuracy;

    private Float accuracy;

    private Integer maxLength;

    private Integer reductionFactor;

    private Integer predictionLength;
}