package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations;

import java.lang.annotation.*;

/**
 * Annotation that gets parsed into additional schema properties for the JsonForms library in the frontend.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
@Repeatable(JsonFormProperties.class)
public @interface JsonFormProperty {

    String key();

    int value() default 0;

    String text() default "";

}
