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
public class SigninRequest {

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
}
