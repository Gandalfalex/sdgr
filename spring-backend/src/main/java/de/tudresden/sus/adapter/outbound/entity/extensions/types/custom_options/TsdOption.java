package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options;

import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.Residual;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.residual.ResidualConverter;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.Season;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.season.SeasonConverter;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.Trend;
import de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.parameter.trend.TrendConverter;
import jakarta.persistence.*;
import lombok.Data;
import lombok.experimental.Accessors;

@Entity(name = "TsdOption")
@Table(name = "tsd_options")
@Data
@Accessors(chain = true)
public class TsdOption {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;


    @Convert(converter = TrendConverter.class)
    private Trend trend;

    @Convert(converter = SeasonConverter.class)
    private Season season;

    @Convert(converter = ResidualConverter.class)
    private Residual residual;
}
