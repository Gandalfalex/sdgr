package de.tudresden.sus.ports;

import de.tudresden.sus.adapter.inbound.dto.DataTypeDTO;
import org.springframework.stereotype.Service;

import javax.xml.crypto.Data;
import java.util.List;

@Service
public interface DataTypeServicePort {
    List<DataTypeDTO> getAllDataTypes();
    DataTypeDTO save(DataTypeDTO entity);
    DataTypeDTO findByName(String name);
    void deleteById(String name);
    DataTypeDTO update(String name, DataTypeDTO entity);
    DataTypeDTO buildCustomizeSchema(DataTypeDTO data);
    DataTypeDTO buildMlModel(DataTypeDTO baseElement, Long configurationId);
    DataTypeDTO buildTSAModel(DataTypeDTO baseElement);

}
