package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.Track;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface TrackRepository extends JpaRepository<Track, Long> {
    @Modifying
    @Transactional
    @Query(value = "DELETE FROM tracks_data_sets WHERE track_id = :trackId AND data_sets_id = :dataSetId", nativeQuery = true)
    void deleteDataSetFromProject(@Param("trackId") Long trackId, @Param("dataSetId") Long dataSetId);

    @Modifying
    @Transactional
    @Query(value = "INSERT INTO tracks_data_sets (track_id, data_sets_id) VALUES (:trackId, :dataSetId) ON CONFLICT DO NOTHING", nativeQuery = true)
    void addDataSetToTrack(@Param("trackId") Long trackId, @Param("dataSetId") Long dataSetId);
}
