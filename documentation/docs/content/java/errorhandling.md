---
title: "Error Handling"
date: 2023-12-08T19:22:33+01:00
tags: []
featured_image: ""
description: ""
---


## ERROR Handling
The Spring application incorporates a robust error handling mechanism through custom exceptions and exception handlers. This approach streamlines error tracking and simplifies the business logic within the application.


- Design: Custom exceptions are designed to encapsulate various error scenarios, allowing for a unified and consistent error response format.
- Extension-Friendly: The format of the custom exception messages is designed to be open to extensions, providing flexibility for future enhancements.

```java
@ControllerAdvice
@Slf4j
public class EntityNotFoundExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ResponseEntity<RestError> handleEntityNotFoundException(EntityNotFoundException ex) {
        log.error("Entity not found: {}", ex.getMessage());
        return new ResponseEntity<>(
            new RestError()
                .setMessage(ex.getMessage())
                .setError("INVALID_ID")
                .setI18nKey("INVALID_ID"), 
            HttpStatus.NOT_FOUND);
    }
}
```
- Reduced Complexity: By using custom exceptions, the business logic is relieved from handling each error scenario individually.
- Streamlined Error Handling: Instead of returning custom errors from each REST method, the business logic can throw the relevant exception, including a detailed reason for the failure.
- Exception Interception: Exception handlers intercept these exceptions and map the provided information onto a custom error message object, maintaining consistency and clarity in error responses.