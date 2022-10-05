package com.vaclav.benchmark.example;

import com.vaclav.benchmark.core.Benchmark;
import com.vaclav.benchmark.core.BenchmarkSet;

@BenchmarkSet(
        types = {BubbleSort.class, QuickSort.class},
        iterations = 5,
        warmingUp = true,
        scenarioDuration = 1000)
public class BubbleVsQuickSortExampleSet {

    public static void main(String[] args) throws Exception {

        Benchmark benchmark = new Benchmark(BubbleVsQuickSortExampleSet.class);
        benchmark.run();
    }
}