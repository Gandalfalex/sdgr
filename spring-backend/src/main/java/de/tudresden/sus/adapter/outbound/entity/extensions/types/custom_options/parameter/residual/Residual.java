package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.NoResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.NormalResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.PoissonResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.strategies.UniformResidual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations.JsonFormProperty;
import lombok.Getter;

import java.util.Random;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME)
@JsonSubTypes({@JsonSubTypes.Type(NoResidual.class), @JsonSubTypes.Type(NormalResidual.class), @JsonSubTypes.Type(UniformResidual.class), @JsonSubTypes.Type(PoissonResidual.class)})
@JsonIgnoreProperties(ignoreUnknown = true)
@Getter
public abstract class Residual {

    @JsonFormProperty(key = "description", text = "The seed for the random number generator. Using the same seed will result in the same values being generated.")
    private long seed;
    public abstract double getValue(int time, boolean multiplicative, Random random);
}
