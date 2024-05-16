package de.tudresden.sus.adapter.inbound.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SignUpRequest {

    @JsonProperty(value = "firstName", required = true)
    @Schema(name = "fistName", description = "name of user")
    @NotNull
    @NotBlank(message = "first name is mandatory")
    @Size(min = 1, max = 30, message = "first name length should not longer than 30")
    private String firstName;

    @JsonProperty(value = "lastName", required = true)
    @Schema(name = "lastName", description = "name of user")
    @NotNull
    @NotBlank(message = "lastname is mandatory")
    @Size(min = 1, max = 30, message = "lastname length should not longer than 30")
    private String lastName;

    @JsonProperty(value = "email", required = true)
    @Schema(name = "email", description = "email of user")
    @NotNull
    @NotBlank(message = "email is mandatory")
    @Size(min = 1, max = 30, message = "email length should not longer than 30")
    private String email;

    @JsonProperty(value = "password", required = true)
    @Schema(name = "password", description = "password of user")
    @NotNull
    @NotBlank(message = "password is mandatory")
    @Size(min = 3, message = "password should be at least 3 symbols long")
    private String password;

    @JsonProperty(value = "languageCode", required = true)
    @Schema(name = "languageCode", description = "preferred language of user")
    @Size(min = 2, max = 2, message = "language code should only contain two elements")
    private String languageCode;
}

