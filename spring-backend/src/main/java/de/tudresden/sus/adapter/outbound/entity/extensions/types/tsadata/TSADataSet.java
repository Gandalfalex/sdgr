package de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.util.DataReducer;
import jakarta.persistence.*;
import java.util.Collections;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.List;

@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Entity
@Accessors(chain = true)
public class TSADataSet extends PlainData {

    @OneToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
    private TSDConfigData tsdConfig;

    @Override
    public DataTypes getDataType() {
        return DataTypes.TSA;
    }

    @Override
    public JsonNode calculatePreviewData(int dataReductionThreshold, DataReducer dataReducer) {
        return null;
    }

    @Override
    public List<String> calculateData() {
        return Collections.emptyList();
    }
}
