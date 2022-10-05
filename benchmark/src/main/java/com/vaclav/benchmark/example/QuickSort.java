package com.vaclav.benchmark.example;

import com.vaclav.benchmark.core.Scenario;
import com.vaclav.benchmark.core.ScenarioAction;

@Scenario
public class QuickSort {

    @ScenarioAction
    public void action(){

        byte[] randomBytesArray = ArrayUtil.getRandomBytesArray();
        quickSort(ArrayUtil.getRandomBytesArray(), 0, randomBytesArray.length - 1);
    }

    private static void swap(byte[] arr, int i, int j) {

        byte temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    private static int partition(byte[] arr, int low, int high) {

        int pivot = arr[high];
        int i = (low - 1);
        for (int j = low; j <= high - 1; j++) {
            if (arr[j] < pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return (i + 1);
    }

   private static void quickSort(byte[] arr, int low, int high) {

        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }
}