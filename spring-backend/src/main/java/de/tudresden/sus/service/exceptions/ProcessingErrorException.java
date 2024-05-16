package de.tudresden.sus.service.exceptions;

import lombok.Getter;

@Getter
public class ProcessingErrorException extends RuntimeException {

    private String message;
    private String i18nCode;
    private int code;


    public ProcessingErrorException(String message, String i18n, int code) {
        super();
        this.message = message;
        this.i18nCode = i18n;
        this.code = code;
    }
}
