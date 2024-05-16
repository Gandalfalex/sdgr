package de.tudresden.sus.adapter.outbound.entity.extensions.types.chardata;


import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.util.DataReducer;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import lombok.experimental.Accessors;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Entity
@Getter
@Setter
@Accessors(chain = true)
@Slf4j
public class CharDataSet extends PlainData {

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "alphabet", joinColumns = @JoinColumn(name = "data_set_id"))
    @Column(name = "character", length = 1, nullable = false)
    private List<String> alphabet;

    @Override
    public DataTypes getDataType() {
        return DataTypes.CHAR;
    }

    @Override
    public JsonNode calculatePreviewData(int dataReductionThreshold, DataReducer dataReducer) {
        return null;
    }

    @Override
    public List<String> calculateData() {
        var values = new ArrayList<String>();
        var random = new Random();
        for (int i = 0; i <= getNumSamples(); i++){

            var value = this.alphabet.get(random.nextInt(alphabet.size()));
            log.info("prepared value: {}", value);
            values.add(value);
        }
        return values;
    }
}

