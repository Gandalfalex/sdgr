package de.tudresden.sus.service.exceptions;

import de.tudresden.sus.adapter.inbound.dto.ErrorMessageDTO;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;


@ControllerAdvice
public class ErrorExceptionHandler {

    @ExceptionHandler(ProcessingErrorException.class)
    public ResponseEntity<ErrorMessageDTO> handleAllExceptions(ProcessingErrorException ex) {
        var error = new ErrorMessageDTO().setMessage(ex.getMessage()).setI18nCode(ex.getI18nCode()).setStatus(ex.getCode());
        return new ResponseEntity<>(error, HttpStatus.valueOf(ex.getCode()));
    }
}
