package de.tudresden.sus.aop;

import de.tudresden.sus.adapter.inbound.errorhandler.InvalidCredentialException;
import de.tudresden.sus.adapter.outbound.entity.User;
import de.tudresden.sus.adapter.outbound.repositories.UserRepository;
import de.tudresden.sus.service.JwtServiceImpl;
import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
@Aspect
@Slf4j
public class UserAspect {


    @Autowired
    private HttpServletRequest request;
    @Autowired
    private JwtServiceImpl service;
    @Autowired
    UserRepository repository;
    // Use this to store user info for the current request thread
    private static final ThreadLocal<User> currentUser = new ThreadLocal<>();

    @Around("@annotation(AttachUser)")
    public Object attachUser(ProceedingJoinPoint joinPoint) throws Throwable {

        User user = extractUserFromJWT();

        if (user != null) {
            currentUser.set(user);
            try {
                return joinPoint.proceed();
            } finally {
                currentUser.remove();  // Clear after method execution
            }
        }

        // If JWT validation fails, you can return an error or throw an exception
        throw new InvalidCredentialException("Invalid JWT token");
    }

    public static User getCurrentUser() {
        return currentUser.get();
    }


    private User extractUserFromJWT() {
        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String jwtToken = authHeader.substring(7);
            return repository.findByEmail(service.extractUserName(jwtToken))
                    .orElseThrow(() -> new InvalidCredentialException("user does not exist"));
        }
        return null;
    }
}