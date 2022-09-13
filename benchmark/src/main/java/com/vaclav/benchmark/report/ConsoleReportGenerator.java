package com.vaclav.benchmark.report;

import com.vaclav.benchmark.core.ScenarioType;
import com.vaclav.benchmark.domain.Report;

public class ConsoleReportGenerator implements ReportGenerator {

    @Override
    public void printReport(Report report) {

        System.out.println("Report results:");
        long[] baseResults = report.getBaseScenarioResults().getResults();
        long[] proposedResults = report.getProposedScenarioResults().getResults();

        if (baseResults.length != proposedResults.length) {
            System.out.println("Unequal length of the base and proposed results! Terminated.");
            System.exit(2);
        }

        System.out.println("Base\t|\t Proposed");
        for (int i = 0; i < baseResults.length; i++) {
            System.out.printf("%d10|%d10\n", baseResults[i], proposedResults[i]);
        }

        System.out.println("Report averages:");

        double baseAverage = report.getAverage(ScenarioType.BASE);
        double proposedAverage = report.getAverage(ScenarioType.PROPOSED);
        System.out.printf("Base: %12.2f\n", baseAverage);
        System.out.printf("Proposed: %12.2f", proposedAverage);
        System.out.println("\n%%");
        System.out.printf("%12.2f", (proposedAverage - baseAverage) / (baseAverage / 100));

        System.out.println("\nReport finished.");
    }
}
