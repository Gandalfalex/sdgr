package de.tudresden.sus.aop;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface FetchTrack {
    String projectIdArgName() default "projectId";
    String trackIdArgName() default "trackId";
}
