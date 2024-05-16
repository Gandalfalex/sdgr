package de.tudresden.sus.adapter.outbound.repositories;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.schema.JSONSchema;
import org.springframework.data.jpa.repository.JpaRepository;

public interface JSONSchemaRepository extends JpaRepository<JSONSchema, Long> {
}
