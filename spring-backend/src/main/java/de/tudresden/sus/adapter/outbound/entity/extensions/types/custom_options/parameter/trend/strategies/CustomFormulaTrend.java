package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.strategies;

import com.fathzer.soft.javaluator.DoubleEvaluator;
import com.fathzer.soft.javaluator.StaticVariableSet;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.Trend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations.JsonFormProperty;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.experimental.Accessors;

@Getter
@Setter
@NoArgsConstructor
@Accessors(chain = true)
public class CustomFormulaTrend implements Trend {

    @JsonFormProperty(key = "description", text = "A custom formula in infix notation using x as the variable. An example expression would be (2^x-1)*sin(pi/4*x)")
    private String formula;
    @Override
    public double getValue(int time, boolean multiplicative) {
        DoubleEvaluator eval = new DoubleEvaluator();
        StaticVariableSet<Double> variables = new StaticVariableSet<Double>();
        variables.set("x", (double) time);
        return eval.evaluate(formula, variables).floatValue();
    }
}
