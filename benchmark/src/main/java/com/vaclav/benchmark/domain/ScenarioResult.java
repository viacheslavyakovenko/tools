package com.vaclav.benchmark.domain;

import java.util.Arrays;
import java.util.concurrent.atomic.AtomicInteger;

public class ScenarioResult {

    public static final int DEFAULT_CAPACITY = 10;

    private final long[] results;

    private final AtomicInteger position;

    public ScenarioResult() {

        this(DEFAULT_CAPACITY);
    }

    public ScenarioResult(int capacity) {

        super();
        results = new long[capacity];
        position = new AtomicInteger(0);
    }

    public Double getAverage() {

        return Arrays.stream(results).average().orElse(Double.NaN);
    }

    public void add(long value) {

        if (position.get() < results.length) {
            results[position.getAndIncrement()] = value;
        } else {
            throw new ArrayIndexOutOfBoundsException("Results are full, you are trying to add value outside the results array!");
        }
    }

    public long[] getResults() {

        return Arrays.stream(results).toArray();
    }
}