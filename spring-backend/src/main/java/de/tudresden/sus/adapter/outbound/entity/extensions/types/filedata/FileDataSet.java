package de.tudresden.sus.adapter.outbound.entity.extensions.types.filedata;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.JsonNodeFactory;
import de.tudresden.sus.adapter.outbound.entity.DataTypes;
import de.tudresden.sus.adapter.outbound.entity.PlainData;
import de.tudresden.sus.adapter.outbound.restclient.models.entity.TrainData;
import de.tudresden.sus.util.DataReducer;
import de.tudresden.sus.util.Point;
import jakarta.persistence.*;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;

@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Entity
@Accessors(chain = true)
public class FileDataSet extends PlainData {

    @ManyToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    private TrainData trainData;

    @Override
    public JsonNode calculatePreviewData(int dataReductionThreshold, DataReducer dataReducer) {
        ArrayList<Point> points = new ArrayList<>();
        var dataValues = trainData.getValues();
        for (int i = 0; i < dataValues.size(); i++){
            points.add(new Point(i, dataValues.get(i)));
        }
        var pointList = points.stream().toList();
        List<Point> reduced = pointList.size() > dataReductionThreshold
                ? dataReducer.reduce( pointList, 0.05d)
                :  pointList;

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
        return trainData.getValues().stream().map(Object::toString).toList();
    }


    @Override
    public DataTypes getDataType() {
        return DataTypes.FILETYPE;
    }
}
