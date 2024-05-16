package de.tudresden.sus.adapter.outbound.entity.extensions;

import com.fasterxml.jackson.databind.JsonNode;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.util.DataReducer;

import java.util.List;

public interface DataTypeOption {

    DataTypes getDataType();

    JsonNode calculatePreviewData(int dataReductionThreshold, DataReducer dataReducer);

    List<String> calculateData();
}
