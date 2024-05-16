package de.tudresden.sus.adapter.outbound.entity.extensions.types.floatdata;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.CalculationMethod;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.TsdOption;
import de.tudresden.sus.util.DataReducer;
import de.tudresden.sus.util.Point;
import jakarta.persistence.*;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Entity
@Accessors(chain = true)
public class FloatDataSet extends PlainData {

    @Enumerated(EnumType.STRING)
    private CalculationMethod calculationMethod;

    @OneToOne(fetch = FetchType.EAGER, orphanRemoval = true, cascade = CascadeType.ALL)
    private TsdOption tsdOption;

    @Override
    public DataTypes getDataType() {
        return DataTypes.FLOAT;
    }

    @Override
    public JsonNode calculatePreviewData(int dataReductionThreshold, DataReducer dataReducer) {
        var preview = new ArrayList<Point>();
        var random = new Random(this.tsdOption.getResidual().getSeed());
        var calculationMethod = this.getCalculationMethod();
        var customValues = this.getCustomValues();

        for (int i = 0; i < this.getNumSamples(); i++) {
            double value;

            if (customValues.containsKey(i)) {
                value = customValues.get(i);
            } else {
                if (calculationMethod == CalculationMethod.MULTIPLICATIVE) {
                    value = this.tsdOption.getTrend().getValue(i, true) * this.tsdOption.getSeason().getValue(i, true) * this.tsdOption.getResidual().getValue(i, true, random);
                } else {
                    value = this.tsdOption.getTrend().getValue(i, false) + this.tsdOption.getSeason().getValue(i, false) + this.tsdOption.getResidual().getValue(i, false, random);
                }
            }

            preview.add(new Point(i, value));
        }

        // reduce data if we are above the threshold
        List<Point> reduced = preview.size() > dataReductionThreshold
                ? dataReducer.reduce(preview, 0.05d)
                : preview;

        var node = JsonNodeFactory.instance.objectNode();
        var labels = JsonNodeFactory.instance.arrayNode();
        var values = JsonNodeFactory.instance.arrayNode();

        for (Point point : reduced) {
            labels.add(point.x());
            values.add(point.y());
        }

        node.set("labels", labels);
        node.set("values", values);

        return node;
    }


    @Override
    public List<String> calculateData() {
        var values = new ArrayList<String>();
        var random = new Random(getTsdOption().getResidual().getSeed());
        var calculationMethod = getCalculationMethod();
        var customValues = getCustomValues();

        for (int i = 0; i < getNumSamples(); i++) {
            double value;

            if (customValues != null && customValues.containsKey(i)) {
                value = customValues.get(i);
            } else {
                if (calculationMethod == CalculationMethod.MULTIPLICATIVE) {
                    value = getTsdOption().getTrend().getValue(i, true) * getTsdOption().getSeason().getValue(i, true) * getTsdOption().getResidual().getValue(i, true, random);
                } else {
                    value = getTsdOption().getTrend().getValue(i, false) + getTsdOption().getSeason().getValue(i, false) + getTsdOption().getResidual().getValue(i, false, random);
                }
            }
            values.add(String.valueOf(value));
        }
        return values;
    }

}
