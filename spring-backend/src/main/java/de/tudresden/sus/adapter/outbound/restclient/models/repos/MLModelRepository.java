package de.tudresden.sus.adapter.outbound.restclient.models.repos;

import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLModels;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.stream.Stream;

public interface MLModelRepository extends JpaRepository<MLModels, Long> {

    @Query("SELECT DISTINCT m FROM MLModels m JOIN MLConfiguration mc ON mc.mlmodel.id = m.id JOIN User u ON u.id = ?1")
    Stream<MLModels> findMlModelByWithConfigurationByUserId(Integer userId);
}
