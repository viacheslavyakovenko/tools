# Benchmarking

Sometimes you need to test different approaches and understand which of them works quicker. And do it in an easy manner. For example, which call execution will be faster - static or virtual? Or, another example - how to quickly check that QuickSort is better than Bubble one?

If you need it for experiments or for your job, you are in the right place. This tiny framework will help for your quick and easy prototyping.

Let’s go! You’ll need two different implementations of some sort of action. In my example there are two implementations of the sorting algorithms - Bubble and QuickSort. You will need two classes with them. Each class should have a public void method without any parameters (It’s a known limitation for current version). Each method should be annotated with @ScenarioAction, and each class with @Scenario. One of them should be “based” and the second one “proposed”. “Based” will be used as a basis for performance calculation. And a performance of the “proposed” will be calculated relatively to it.

```
@Scenario(scenarioType = ScenarioType.BASE)
public class BubbleSort {

    @ScenarioAction
    public void action() throws NoSuchAlgorithmException {

        bubbleSort(ArrayUtil.getRandomBytesArray());
    }
…
```
```
@Scenario(scenarioType = ScenarioType.PROPOSED)
public class QuickSort {

    @ScenarioAction
    public void action(){

        byte[] randomBytesArray = ArrayUtil.getRandomBytesArray();
        quickSort(ArrayUtil.getRandomBytesArray(), 0, randomBytesArray.length - 1);
    }
…
```
After that you need to create a runner which will run two benchmarks and compare the results:
```
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
```

So, it’s easy:
1. Create two implementations
2. Mark them as @Scenario & @ScenarioAction
3. Create an @BenchmarkSet class
4. Start runner