package de.tudresden.sus.adapter.outbound.restclient.models.repos;

import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLSolution;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLTrainingInformation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface MLTrainingsInformationRepository extends JpaRepository<MLTrainingInformation, Long> {
    Optional<MLTrainingInformation> findMLTrainingInformationByMlSolution(MLSolution solution);
}
