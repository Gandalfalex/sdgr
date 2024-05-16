package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TsdLevelTrainData;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TsdLevelTrainDataRepository extends JpaRepository<TsdLevelTrainData, Long> {

}
