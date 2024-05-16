package de.tudresden.sus.adapter.inbound.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;
import lombok.experimental.Accessors;

/**
 * Data transfer object for representing projects when communicating via the API.
 */
@Data
@Accessors(chain = true)
public class ProjectDTO {

    private long id;

    @NotNull
    @NotBlank(message = "name is mandatory")
    @Size(min = 2, max = 30)
    private String name;

    private boolean sending;

}
