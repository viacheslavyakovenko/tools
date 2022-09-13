package com.vaclav.benchmark.core;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface BenchmarkSet {

    static final int MIN_DURATION_MS = 1000;

    static final int ITERATIONS = 1;

    Class[] types();

    boolean warmingUp() default true;

    int warmingUpDuration() default MIN_DURATION_MS;

    int scenarioDuration() default MIN_DURATION_MS;

    int iterations() default ITERATIONS;
}