package de.tudresden.sus.adapter.outbound.entity.extensions.types.mldata;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.tsadata.TSDConfigData;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.MLConfiguration;
import de.tudresden.sus.util.DataReducer;
import jakarta.persistence.*;
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
public class MlDataSet extends PlainData {

    @OneToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL, orphanRemoval = true)
    private MlConfigData mlConfig;

    @Override
    public DataTypes getDataType() {
        return DataTypes.ML;
    }

    @Override
    public JsonNode calculatePreviewData(int dataReductionThreshold, DataReducer dataReducer) {
        return null;
    }

    @Override
    public List<String> calculateData() {
        return null;
    }
}
