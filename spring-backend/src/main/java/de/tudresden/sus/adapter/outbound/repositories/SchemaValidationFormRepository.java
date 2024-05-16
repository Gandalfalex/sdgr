package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.schema.SchemaValidationForms;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface SchemaValidationFormRepository extends JpaRepository<SchemaValidationForms, Long> {

    Optional<SchemaValidationForms> findFirstByName(String name);
}
