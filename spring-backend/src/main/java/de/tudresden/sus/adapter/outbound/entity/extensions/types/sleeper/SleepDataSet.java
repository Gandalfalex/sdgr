package de.tudresden.sus.adapter.outbound.entity.extensions.types.sleeper;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.util.DataReducer;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
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
public class SleepDataSet extends PlainData {

    @Column(name = "sleep_time")
    private int sleepTime;

    @Override
    public DataTypes getDataType() {
        return DataTypes.SLEEP;
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
