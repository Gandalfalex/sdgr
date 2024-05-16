package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.PlainData;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;


public interface PlainDataRepository extends JpaRepository<PlainData, Long> {


    @Query(value = "SELECT p.id, t.id, pd.id, p.name, t.name, pd.name " +
            "FROM plain_data pd " +
            "JOIN tracks_data_sets tds ON tds.data_sets_id = pd.id " +
            "JOIN projects_tracks pt ON pt.tracks_id = tds.track_id " +
            "JOIN tracks t ON t.id  = tds.track_id " +
            "JOIN projects p ON p.id = pt.project_id " +
            "JOIN ml_config_data m on m.id = pd.ml_config_id " +
            "WHERE m.ml_configuration_id = :config AND p.user_id = :user", nativeQuery = true)
    List<Object[]> findAllMlByMLConfigurationId(@Param("config") Long id, @Param("user") Integer user);

    @Query(value = "SELECT p.id, t.id, pd.id, p.name, t.name, pd.name " +
            "FROM plain_data pd " +
            "JOIN tracks_data_sets tds ON tds.data_sets_id = pd.id " +
            "JOIN projects_tracks pt ON pt.tracks_id = tds.track_id " +
            "JOIN tracks t ON t.id  = tds.track_id " +
            "JOIN projects p ON p.id = pt.project_id " +
            "JOIN tsdconfig_data td ON td.id = pd.tsd_config_id " +
            "JOIN tsd_configuration tc ON td.tsd_config = tc.id " +
            "WHERE tc.id = :config AND p.user_id = :user", nativeQuery = true)
    List<Object[]> findAllTSDByTSDConfigurationId(@Param("config") Long id, @Param("user") Integer user);

}
