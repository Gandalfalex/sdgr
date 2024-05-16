package de.tudresden.sus.adapter.outbound.restclient.models.entity;


import jakarta.persistence.*;
import lombok.Getter;
import org.hibernate.annotations.Immutable;


@Entity
@Table(name = "ml_solution")
@Immutable
@Getter
public class MLSolution {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.EAGER, orphanRemoval = true)
    @JoinColumn(name = "ml_configuration_id", referencedColumnName = "id")
    private MLConfiguration mlConfiguration;

}