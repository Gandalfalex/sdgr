package de.tudresden.sus.adapter.inbound.errorhandler;

public class DataConversionException extends RuntimeException{
    public DataConversionException(String message) {
        super(message);
    }
}
