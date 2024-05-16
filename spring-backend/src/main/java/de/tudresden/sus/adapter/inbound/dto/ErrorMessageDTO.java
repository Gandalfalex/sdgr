package de.tudresden.sus.adapter.inbound.dto;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class ErrorMessageDTO {

    private String message;
    private String i18nCode;
    private int status;


}
