package de.tudresden.sus.ports;

import org.springframework.security.core.userdetails.UserDetailsService;

public interface UserServicePort {
    UserDetailsService userDetailsService();
}