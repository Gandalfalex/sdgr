package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSDConfigData;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.TSDConfiguration;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface TSDConfigDataRepository extends JpaRepository<TSDConfigData, Long> {

    Optional<TSDConfigData> findByConfiguration(TSDConfiguration configuration);
}
