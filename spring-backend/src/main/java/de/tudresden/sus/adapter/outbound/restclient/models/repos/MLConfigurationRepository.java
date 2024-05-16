package de.tudresden.sus.adapter.outbound.restclient.models.repos;

import de.tudresden.sus.aop.AttachUser;
import de.tudresden.sus.aop.UserAspect;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLConfiguration;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLModels;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface MLConfigurationRepository extends JpaRepository<MLConfiguration, Long> {

    @AttachUser
    default List<MLConfiguration> findAllByMlmodel(MLModels model) {
        User user = UserAspect.getCurrentUser();
        return findAllByUserAndMlmodel(user, model);
    }

    @Override
    @AttachUser
    default Optional<MLConfiguration> findById(Long id){
        User user = UserAspect.getCurrentUser();
        return findByIdAndUser(id, user);
    }

    @AttachUser
    default List<MLConfiguration> findAll(){
        User user = UserAspect.getCurrentUser();
        return findAllByUser(user);
    }

    Optional<MLConfiguration> findByIdAndUser(Long id, User user);

    List<MLConfiguration> findAllByUser(User user);

    List<MLConfiguration> findAllByUserAndMlmodel(User user, MLModels models);
}
