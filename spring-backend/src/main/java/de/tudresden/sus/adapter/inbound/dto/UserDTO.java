package de.tudresden.sus.adapter.inbound.dto;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class UserDTO {

    public String name;
    public String mail;

}
