package de.tudresden.sus.adapter.inbound.errorhandler;

public class InvalidCredentialException extends RuntimeException {

    public InvalidCredentialException(String message) {
        super(message);
    }
}
