package de.tudresden.sus.adapter.outbound.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import java.util.Set;

@Data
@NoArgsConstructor
@Entity(name = "Track")
@Table(name = "tracks")
@Accessors(chain = true)
public class Track {

    @Id
    @Column
    @GeneratedValue(strategy = GenerationType.AUTO)
    @JsonIgnore
    private Long id;

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.EAGER, orphanRemoval = true)
    @OrderBy("position")
    private Set<PlainData> dataSets;

    @ManyToMany(fetch = FetchType.LAZY)
    private Set<DataType> allowedDataTypes;

    @Column
    private boolean repeating;

    @Column
    private String name;

    @Column
    private String unit;

    @Override
    public String toString() {
        return "Track{" +
                "id=" + id +
                ", dataSets=" + dataSets +
                ", allowedDataTypes=" + allowedDataTypes.stream().map(DataType::getName).toList() +
                ", repeating=" + repeating +
                ", name='" + name + '\'' +
                ", unit='" + unit + '\'' +
                '}';
    }
}
