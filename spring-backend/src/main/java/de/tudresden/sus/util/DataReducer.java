package de.tudresden.sus.util;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * Ramer-Douglas-Peucker algorithm implementation adapted from <a href="https://github.com/phishman3579/java-algorithms-implementation/blob/master/src/com/jwetherell/algorithms/mathematics/RamerDouglasPeucker.java">here</a>
 */
@Service
@Slf4j
public class DataReducer {

    private double square(double x) {
        return x * x;
    }

    private double distance(Point a, Point b) {
        return square(a.x() - b.x()) + square(a.y() - b.y());
    }

    private double distanceToSegmentSquared(Point point, Point start, Point end) {
        var l2 = distance(start, end);
        if (l2 == 0) {
            return distance(point, start);
        }

        var t = ((point.x() - start.x()) * (end.x() - start.x()) + (point.y() - start.y()) * (end.y() - start.y())) / l2;
        if (t < 0) {
            return distance(point, start);
        }
        if (t > 1) {
            return distance(point, end);
        }

        var l = new Point(start.x() + t * (end.x() - start.x()), start.y() + t * (end.y() - start.y()));
        return distance(point, l);
    }

    private double perpendicularDistance(Point point, Point start, Point end) {
        return Math.sqrt(distanceToSegmentSquared(point, start, end));
    }

    private void reduce(List<Point> input, int start, int e, double epsilon, List<Point> output) {
        double dmax = 0;
        int index = 0;

        int end = e - 1;
        for (int i = start + 1; i < end; i++) {
            var point = input.get(i);
            var startPoint = input.get(start);
            var endPoint = input.get(end);

            var distance = perpendicularDistance(point, startPoint, endPoint);
            if (distance > dmax) {
                index = i;
                dmax = distance;
            }
        }

        if (dmax > epsilon) {
            reduce(input, start, index, epsilon, output);
            reduce(input, index, e, epsilon, output);
        } else {
            if ((end - start) > 0) {
                output.add(input.get(start));
                output.add(input.get(end));
            } else {
                output.add(input.get(start));
            }
        }
    }

    public List<Point> reduce(List<Point> input, double epsilon) {
        var output = new ArrayList<Point>();
        reduce(input, 0, input.size(), epsilon, output);
        return output;
    }

}
