package de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata;

import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class CharDataSetMapper {

    @SneakyThrows
    public CharDataSetDTO toDTO(CharDataSet eo) {
        return new CharDataSetDTO()
                .setAlphabet(eo.getAlphabet());
    }

    public CharDataSet toEO(CharDataSetDTO dto){
        return mergeDoToEo((CharDataSet) new CharDataSet().setId(dto.getId()), dto);
    }

    public CharDataSet mergeDoToEo(CharDataSet eo, CharDataSetDTO dto){
        return eo
                .setAlphabet(dto.getAlphabet());
    }
}
