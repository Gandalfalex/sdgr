package de.tudresden.sus.adapter.inbound.errorhandler;

import de.tudresden.sus.security.authentification.RestError;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
@Slf4j
public class DataConversionExceptionHandler {
    @ExceptionHandler(DataConversionException.class)
    public ResponseEntity<RestError> handleDataConversionException(DataConversionException ex) {
        log.error("Data Conversion failed: {}", ex.getMessage());
        return new ResponseEntity<>(new RestError()
                .setMessage(ex.getMessage())
                .setError("conversion of data failed")
                .setI18nKey("CONVERSION_ERROR"), HttpStatus.NOT_FOUND);
    }
}
