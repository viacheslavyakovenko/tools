package com.vaclav.benchmark.example;

import com.vaclav.benchmark.core.Scenario;
import com.vaclav.benchmark.core.ScenarioAction;
import com.vaclav.benchmark.core.ScenarioType;

import java.security.NoSuchAlgorithmException;

@Scenario(scenarioType = ScenarioType.PROPOSED)
public class BubbleSort {

    @ScenarioAction
    public void action() throws NoSuchAlgorithmException {

        bubbleSort(ArrayUtil.getRandomBytesArray());
    }

    static void bubbleSort(byte arr[]) {

        int n = arr.length;
        byte i, j, temp;
        boolean swapped;
        for (i = 0; i < n - 1; i++) {
            swapped = false;
            for (j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    // swap arr[j] and arr[j+1]
                    temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            if (swapped == false)
                break;
        }
    }
}