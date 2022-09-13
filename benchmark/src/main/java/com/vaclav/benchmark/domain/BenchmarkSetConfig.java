package com.vaclav.benchmark.domain;

import com.vaclav.benchmark.core.BenchmarkSet;
import com.vaclav.benchmark.core.Scenario;
import com.vaclav.benchmark.core.ScenarioType;

import java.lang.annotation.Annotation;
import java.lang.reflect.Constructor;
import java.lang.reflect.InvocationTargetException;

public class BenchmarkSetConfig {

    private final boolean warmingUp;
    private final int warmingUpDuration;
    private final int scenarioDuration;
    private final int iterations;
    @SuppressWarnings("rawtypes")
    private final Class[] types;

    public static Object[] getScenarios(BenchmarkSetConfig config)
            throws NoSuchMethodException, InvocationTargetException, InstantiationException, IllegalAccessException {

        Class[] types = config.getTypes();
        Object[] result = new Object[types.length];
        for (int i = 0; i < types.length; i++) {

            Constructor constructor = types[i].getConstructor();
            Object scenario = constructor.newInstance();
            result[i] = scenario;
        }
        return result;
    }

    public static ScenarioType resolveScenarioType(@SuppressWarnings("rawtypes") Class clazz) {

        Annotation[] annotations = clazz.getAnnotations();
        for (Annotation a : annotations) {
            Class<? extends Annotation> aClass = a.annotationType();
            if (aClass.equals(Scenario.class)) {
                Scenario scenario = (Scenario) a;
                return scenario.scenarioType();
            }
        }

        return null; //FIXME: handle unset Scenario case
    }

    public BenchmarkSetConfig(@SuppressWarnings("rawtypes") Class clazz) {

        BenchmarkSet benchmarkSet = null;
        for (Annotation a : clazz.getAnnotations()) {
            if (a.annotationType().equals(BenchmarkSet.class)) {
                benchmarkSet = (BenchmarkSet) a;
                break;
            }
        }

        if (benchmarkSet == null) {
            throw new IllegalArgumentException(
                    "Benchmark set should be annotated by @BenchmarkSet annotation");
        } else {
            this.warmingUp = benchmarkSet.warmingUp();
            this.warmingUpDuration = benchmarkSet.warmingUpDuration();
            this.scenarioDuration = benchmarkSet.scenarioDuration();
            this.types = benchmarkSet.types();
            this.iterations = benchmarkSet.iterations();
        }
    }

    public boolean isWarmingUp() {
        return warmingUp;
    }

    public int getWarmingUpDuration() {
        return warmingUpDuration;
    }

    public int getScenarioDuration() {
        return scenarioDuration;
    }

    @SuppressWarnings("rawtypes")
    public Class[] getTypes() {
        return types;
    }

    public int getIterations() {
        return iterations;
    }
}