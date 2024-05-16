package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.Project;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;
import java.util.Optional;

import static org.hibernate.query.sqm.tree.SqmNode.log;


public interface ProjectRepository extends JpaRepository<Project, Long> {


    @Override
    @AttachUser
    default Optional<Project> findById(Long id) {
        User user = UserAspect.getCurrentUser();
        return findByIdAndUser(id, user);
    }

    @Override
    @AttachUser
    default List<Project> findAll() {
        User user = UserAspect.getCurrentUser();
        return findAllByUser(user);
    }

    @Transactional(Transactional.TxType.REQUIRES_NEW)
    Optional<Project> findByIdAndUser(Long id, User user);

    List<Project> findAllByUser(User user);

    @Modifying
    @Transactional
    @Query(value = "INSERT INTO projects_tracks (project_id, tracks_id) VALUES (:projectId, :trackId) ON CONFLICT DO NOTHING", nativeQuery = true)
    void addTrackToProject(Long projectId, Long trackId);

    @Modifying
    @Transactional
    @Query(value = "DELETE FROM projects_tracks WHERE project_id = :projectId AND tracks_id = :trackId", nativeQuery = true)
    void deleteTrackFromProject(@Param("projectId") Long projectId, @Param("trackId") Long trackId);

    @Query("SELECT p FROM Project p JOIN FETCH p.tracks WHERE p.id = :projectId")
    Optional<Project> findByIdWithTracks(@Param("projectId") Long projectId);

}
