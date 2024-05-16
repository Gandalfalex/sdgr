package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.LogMessage;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface LogMessageRepository extends JpaRepository<LogMessage, Long> {

    List<LogMessage> findByTrackId(Long trackId);

    Page<LogMessage> findByTrackId(Long trackId, Pageable pageable);

    @Query(value = "SELECT * FROM log_messages l WHERE l.track_id = :track AND (l.message LIKE %:value% OR l.send_session LIKE %:value% OR l.data_set_name LIKE %:value% OR TO_CHAR(l.time_stamp, 'HH24:MI:SS:MS (0F)') LIKE %:value%)", nativeQuery = true)
    Page<LogMessage> findByQueryWithPage(@Param("track") Long trackId, @Param("value")String value, Pageable pageable);

    @Query(value = "SELECT * FROM log_messages l WHERE l.track_id = :track AND (l.message LIKE %:value% OR l.send_session LIKE %:value% OR l.data_set_name LIKE %:value% OR TO_CHAR(l.time_stamp, 'HH24:MI:SS:MS (0F)') LIKE %:value%)", nativeQuery = true)
    List<LogMessage> findByQuery(@Param("track") Long trackId, @Param("value")String value);

    @Query(value = "SELECT count(*) FROM log_messages l WHERE l.track_id = :track AND (l.message LIKE %:value% OR l.send_session LIKE %:value% OR l.data_set_name LIKE %:value% OR TO_CHAR(l.time_stamp, 'HH24:MI:SS:MS (0F)') LIKE %:value%)", nativeQuery = true)
    int countBySearchQuery(@Param("track") Long trackId, @Param("value")String value);
    @Query(value = "SELECT DISTINCT send_session FROM log_messages l WHERE l.track_id = :track", nativeQuery = true)
    List<String> findAllSessionsByTrackId(@Param("track") Long trackId);

    List<LogMessage> findAllByTrackIdAndSendSession(Long trackId, String sendSession);

    int countByTrackId(Long trackId);

    void deleteAllByTrackId(Long trackId);
}
