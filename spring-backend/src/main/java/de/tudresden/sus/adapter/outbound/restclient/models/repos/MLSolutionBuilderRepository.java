package de.tudresden.sus.adapter.outbound.restclient.models.repos;

import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLConfiguration;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLSolution;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface MLSolutionBuilderRepository extends JpaRepository<MLSolution, Long> {
    Optional<MLSolution> findByMlConfiguration(MLConfiguration configuration);
}
