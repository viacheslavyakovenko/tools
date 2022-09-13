package com.vaclav.benchmark.core;

import com.vaclav.benchmark.domain.BenchmarkSetConfig;
import com.vaclav.benchmark.domain.Report;
import com.vaclav.benchmark.report.ConsoleReportGenerator;
import com.vaclav.benchmark.report.ReportGenerator;

public class Benchmark {

    private final BenchmarkSetConfig config;

    private final Report report;

    private final ReportGenerator reportGenerator;

    public Benchmark(@SuppressWarnings("rawtypes") Class benchmarkSet) {

        this.config = new BenchmarkSetConfig(benchmarkSet);
        this.report = new Report(config.getIterations());

        //TODO: make it configurable
        this.reportGenerator = new ConsoleReportGenerator();
    }

    public void run() throws Exception {

        doBenchmarkSet();
        this.reportGenerator.printReport(this.report);
    }

    void doBenchmarkSet() throws Exception {

        Object[] scenarios = BenchmarkSetConfig.getScenarios(config);
        if (scenarios == null || scenarios.length < 2) {
            System.out.println("Scenarios list is empty! Exited!");
            System.exit(1);
        }

        if (config.isWarmingUp()) {
            System.out.println("Please wait! I'm warming...");
            doBenchmark(config, true);
        }

        System.out.println("Benchmark started...");
        for (int i = 0; i < config.getIterations(); i++) {
            doBenchmark(config, false);
        }
        System.out.println("Benchmark finished.");
    }

    void doBenchmark(BenchmarkSetConfig config, boolean warming) throws Exception {

        Object[] scenarios = BenchmarkSetConfig.getScenarios(config);
        for (Object scenario : scenarios) {
            if (warming) {
                runScenario(ScenarioRunner.DEFAULT_DURATION, scenario);
            } else {
                long iterations =
                        runScenario(config.getScenarioDuration(), scenario);
                ScenarioType scenarioType =
                        BenchmarkSetConfig.resolveScenarioType(scenario.getClass());
                if (scenarioType == ScenarioType.BASE) {
                    this.report.add(scenarioType, iterations);
                } else if (scenarioType == ScenarioType.PROPOSED) {
                    this.report.add(scenarioType, iterations);
                }
            }
        }
    }

    long runScenario(int duration, Object scenario) throws Exception {

        ScenarioRunner scenarioRunner = new ScenarioRunner(scenario);
        scenarioRunner.setTerminate(false);
        scenarioRunner.setCount(0L);
        Thread thread = new Thread(scenarioRunner);
        thread.start();
        Thread.sleep(duration);
        scenarioRunner.setTerminate(true);
        thread.join();

        return scenarioRunner.getCount();
    }

}