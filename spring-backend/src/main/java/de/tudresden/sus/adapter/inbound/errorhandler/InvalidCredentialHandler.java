package de.tudresden.sus.adapter.inbound.errorhandler;

import de.tudresden.sus.security.authentification.RestError;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class InvalidCredentialHandler {

    @ExceptionHandler(InvalidCredentialException.class)
    public ResponseEntity<RestError> handleInvalidCredentialException(InvalidCredentialException ex) {
        return new ResponseEntity<>(new RestError()
                .setError("Unauthorized")
                .setMessage(ex.getMessage())
                .setI18nKey("UNAUTHORIZED"), HttpStatus.FORBIDDEN);
    }
}
