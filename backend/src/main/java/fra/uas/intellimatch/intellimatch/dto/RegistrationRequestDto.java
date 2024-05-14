package fra.uas.intellimatch.intellimatch.dto;

import io.swagger.v3.oas.annotations.media.Schema;

@Schema(description = "DTO for user registration")
public record RegistrationRequestDto(
        @Schema(example = "newuser", description = "Username for the new user")
        String username,

        @Schema(example = "newuser@example.com", description = "Email address of the new user")
        String email,

        @Schema(example = "securePassword123", description = "Password for the new user")
        String password) {
}
