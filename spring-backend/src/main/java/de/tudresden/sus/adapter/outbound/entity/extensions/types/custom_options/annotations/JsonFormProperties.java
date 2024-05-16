package de.tudresden.sus.adapter.outbound.entity.extensions.types.custom_options.annotations;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Utility annotation to support multiple {@link  JsonFormProperty} annotations on a single field.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface JsonFormProperties {
    JsonFormProperty[] value();
}
