package de.tudresden.sus.adapter.outbound.mapper;

import de.tudresden.sus.adapter.inbound.dto.DataTypeDTO;
import de.tudresden.sus.adapter.outbound.entity.DataType;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.weaver.loadtime.Agent;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
@Slf4j
public class DataTypeMapper {


    public DataTypeDTO toDTO(DataType entity) {
        return new DataTypeDTO().setName(entity.getName())
                .setDescription(entity.getDescription())
                .setPreviewVisible(entity.isPreviewVisible())
                .setType(entity.getType())
                .setSchema(entity.getSchema().getSchema())
                .setUiSchema(entity.getSchema().getUiSchema());
    }

    public DataType fromDTO(DataTypeDTO dto) {
        DataType entity = new DataType();
        entity.setName(dto.getName())
                .setDescription(dto.getDescription())
                .setPreviewVisible(dto.isPreviewVisible())
                .setType(dto.getType());
        return entity;
    }

}

