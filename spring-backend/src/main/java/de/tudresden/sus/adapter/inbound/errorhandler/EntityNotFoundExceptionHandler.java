package de.tudresden.sus.adapter.inbound.errorhandler;

import de.tudresden.sus.security.authentification.RestError;
import jakarta.persistence.EntityNotFoundException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
@Slf4j
public class EntityNotFoundExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<RestError> handleEntityNotFoundException(EntityNotFoundException ex) {
        log.error("Entity not found: {}", ex.getMessage());
        return new ResponseEntity<>(new RestError()
                .setMessage(ex.getMessage())
                .setError("INVALID_ID")
                .setI18nKey("INVALID_ID"), HttpStatus.NOT_FOUND);
    }
}
