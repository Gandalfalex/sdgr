package de.tudresden.sus.adapter.outbound.restclient.models.repos;

import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.TrainData;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface TrainDataRepository extends JpaRepository<TrainData, Long> {

    @AttachUser
    default Optional<TrainData> findById(Long id){
        User user = UserAspect.getCurrentUser();
        return findByIdAndUser(id, user);
    }

    Optional<TrainData> findByIdAndUser(Long id, User user);
}
