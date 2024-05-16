package de.tudresden.sus.adapter.outbound.restclient.models.repos;

import de.tudresden.sus.adapter.outbound.restclient.models.entity.TSDModel;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;
import java.util.stream.Stream;

public interface TSDModelRepository extends JpaRepository<TSDModel, Long> {

    @Query("SELECT DISTINCT m FROM TSDModel m JOIN TSDConfiguration mc ON mc.tsdModel.id = m.id JOIN User u ON u.id = ?1")
    Stream<TSDModel> findTSDModelByWithConfigurationByUserId(Integer userId);
}
