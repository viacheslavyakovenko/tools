package com.vaclav.benchmark.domain;

import com.vaclav.benchmark.core.ScenarioType;

public class Report {

    private final ScenarioResult baseScenarioResults;

    private final ScenarioResult proposedScenarioResults;

    public Report(int iterations) {

        this.baseScenarioResults = new ScenarioResult(iterations);
        this.proposedScenarioResults = new ScenarioResult(iterations);
    }

    public void add(ScenarioType scenarioType, long value) {

        if (scenarioType.equals(ScenarioType.BASE)) {
            baseScenarioResults.add(value);
        } else if (scenarioType.equals(ScenarioType.PROPOSED)) {
            proposedScenarioResults.add(value);
        }
    }

    public Double getAverage(ScenarioType scenarioType) {

        if (scenarioType.equals(ScenarioType.BASE)) {
            return this.baseScenarioResults.getAverage();
        } else if (scenarioType.equals(ScenarioType.PROPOSED)) {
            return this.proposedScenarioResults.getAverage();
        }
        return 0D;
    }

    public ScenarioResult getBaseScenarioResults() {

        return baseScenarioResults;
    }

    public ScenarioResult getProposedScenarioResults() {

        return proposedScenarioResults;
    }
}