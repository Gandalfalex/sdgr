package de.tudresden.sus.adapter.outbound.restclient.models.dto;

import lombok.Data;
import lombok.experimental.Accessors;

import java.util.List;
@Data
@Accessors(chain = true)
public class SignalDataDTO {
    private String name;
    private List<String> data;

}
