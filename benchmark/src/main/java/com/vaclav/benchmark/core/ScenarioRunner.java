package com.vaclav.benchmark.core;

import java.lang.annotation.Annotation;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class ScenarioRunner implements Runnable {

    private volatile boolean terminate = false;

    private long count = 0;

    private final Object scenario;

    public static int DEFAULT_DURATION = 1000; // ms

    public ScenarioRunner(Object scenario) {
        this.scenario = scenario;
    }

    public boolean isTerminate() {
        return terminate;
    }

    public void setTerminate(boolean terminate) {
        this.terminate = terminate;
    }

    public long getCount() {
        return count;
    }

    public void setCount(long count) {
        this.count = count;
    }

    public static Method getScenarioAction(Object scenario) {

        Method[] methods = scenario.getClass().getMethods();
        for (Method method : methods) {
            Annotation[] annotations = method.getAnnotations();
            for (Annotation a : annotations) {
                if (a.annotationType().equals(ScenarioAction.class)
                        && method.getReturnType().equals(void.class)
                        && method.getParameterCount() == 0) {
                    return method;
                }
            }
        }

        throw new IllegalArgumentException(
                "Object doesn't have method annotated with @ScenarioAction!");
    }

    @Override
    public void run() {

        Method action = ScenarioRunner.getScenarioAction(scenario);
        long count = 0L;
        while (!this.isTerminate()) {
            try {
                action.invoke(scenario);
            } catch (IllegalAccessException | InvocationTargetException e) {
                throw new RuntimeException(e);
            }
            count++;
        }
        this.setCount(count);
    }
}