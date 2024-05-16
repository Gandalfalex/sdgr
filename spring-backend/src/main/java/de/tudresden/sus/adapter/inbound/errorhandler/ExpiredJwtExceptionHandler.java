package de.tudresden.sus.adapter.inbound.errorhandler;

import de.tudresden.sus.security.authentification.RestError;
import io.jsonwebtoken.ExpiredJwtException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class ExpiredJwtExceptionHandler {
    @ExceptionHandler(ExpiredJwtException.class)
    public ResponseEntity<RestError> handleExpiredJwtException(ExpiredJwtException ex) {
        return new ResponseEntity<>(new RestError().setError("Unauthorized").setMessage(ex.getMessage()).setI18nKey("JWT_EXPIRED"), HttpStatus.FORBIDDEN);
    }
}
