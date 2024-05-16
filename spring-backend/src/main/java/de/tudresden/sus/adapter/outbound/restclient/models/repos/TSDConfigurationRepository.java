package de.tudresden.sus.adapter.outbound.restclient.models.repos;

import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.TSDConfiguration;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.TSDModel;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface TSDConfigurationRepository extends JpaRepository<TSDConfiguration, Long> {
    @AttachUser
    default List<TSDConfiguration> findAllByTsdModel(TSDModel model) {
        User user = UserAspect.getCurrentUser();
        return findAllByUserAndTsdModel(user, model);
    }

    @AttachUser
    default Optional<TSDConfiguration> findById(Long id){
        User user = UserAspect.getCurrentUser();
        return findByIdAndUser(id, user);
    }

    @AttachUser
    default List<TSDConfiguration> findAll(){
        User user = UserAspect.getCurrentUser();
        return findAllByUser(user);
    }

    Optional<TSDConfiguration> findByIdAndUser(Long id, User user);

    List<TSDConfiguration> findAllByUser(User user);

    List<TSDConfiguration> findAllByUserAndTsdModel(User user, TSDModel models);
}
