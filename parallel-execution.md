# Parallel Execution

## Overview

The Parallel Execution pattern enables concurrent execution of multiple activities or child workflows to maximize throughput and minimize total execution time. Using Temporal's Promise API, you can launch multiple operations asynchronously and wait for their completion.

## Problem

In sequential execution, operations run one after another, causing unnecessary delays when:
- Multiple independent operations could run simultaneously
- Total execution time equals the sum of all operation durations
- Resources (workers, external services) sit idle while waiting
- User experience suffers from slow response times
- Batch processing takes hours when it could take minutes

Without parallel execution, you must:
- Accept slow, sequential processing
- Implement complex threading or async logic manually
- Risk inconsistent state management across threads
- Handle thread safety and synchronization issues

## Solution

Temporal's `Async.function()` and `Promise.allOf()` enable launching multiple activities or child workflows concurrently. Each operation returns a Promise that resolves when complete. Use `Promise.allOf()` to wait for all operations or `Promise.anyOf()` for the first completion.

## Implementation

### Basic Parallel Activities

```java
@WorkflowInterface
public interface ParallelWorkflow {
  @WorkflowMethod
  List<String> processInParallel(List<String> items);
}

public class ParallelWorkflowImpl implements ParallelWorkflow {
  private final ProcessingActivity activity = 
    Workflow.newActivityStub(ProcessingActivity.class);
  
  @Override
  public List<String> processInParallel(List<String> items) {
    List<Promise<String>> promises = new ArrayList<>();
    
    for (String item : items) {
      Promise<String> promise = Async.function(activity::process, item);
      promises.add(promise);
    }
    
    Promise.allOf(promises).get();
    return promises.stream().map(Promise::get).collect(Collectors.toList());
  }
}
```

### Parallel Child Workflows

```java
public class ParallelChildWorkflowImpl implements ParallelWorkflow {
  
  @Override
  public List<Result> processInParallel(List<Task> tasks) {
    List<Promise<Result>> promises = new ArrayList<>();
    
    for (Task task : tasks) {
      ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class);
      Promise<Result> promise = Async.function(child::execute, task);
      promises.add(promise);
    }
    
    Promise.allOf(promises).get();
    return promises.stream().map(Promise::get).collect(Collectors.toList());
  }
}
```

### Advanced: Controlled Parallelism

```java
public class BatchWorkflowImpl implements BatchWorkflow {
  private final ProcessingActivity activity = 
    Workflow.newActivityStub(ProcessingActivity.class);
  
  @Override
  public BatchResult processBatch(List<String> items, int maxParallel) {
    List<String> results = new ArrayList<>();
    
    for (int i = 0; i < items.size(); i += maxParallel) {
      int end = Math.min(i + maxParallel, items.size());
      List<String> batch = items.subList(i, end);
      
      List<Promise<String>> promises = batch.stream()
        .map(item -> Async.function(activity::process, item))
        .collect(Collectors.toList());
      
      Promise.allOf(promises).get();
      results.addAll(promises.stream().map(Promise::get).collect(Collectors.toList()));
    }
    
    return new BatchResult(results);
  }
}
```

### Error Handling

```java
public class ResilientParallelWorkflowImpl implements ParallelWorkflow {
  
  @Override
  public ProcessingReport processWithErrorHandling(List<String> items) {
    List<Promise<Result>> promises = new ArrayList<>();
    
    for (String item : items) {
      Promise<Result> promise = Async.function(() -> {
        try {
          return activity.process(item);
        } catch (Exception e) {
          return Result.failed(item, e.getMessage());
        }
      });
      promises.add(promise);
    }
    
    Promise.allOf(promises).get();
    
    List<Result> results = promises.stream().map(Promise::get).collect(Collectors.toList());
    return new ProcessingReport(results);
  }
}
```

## Key Components

1. **Async.function()**: Executes activity or child workflow asynchronously
2. **Promise**: Represents future result of async operation
3. **Promise.allOf()**: Waits for all promises to complete
4. **Promise.anyOf()**: Waits for first promise to complete
5. **Promise.get()**: Retrieves result (blocks until ready)

## When to Use

**Ideal for:**
- Processing independent items in batches
- Calling multiple external services simultaneously
- Fan-out/fan-in patterns
- Parallel data transformations
- Concurrent API requests
- Multi-step pipelines with independent stages

**Not ideal for:**
- Operations with dependencies between them
- Resource-constrained environments (use controlled parallelism)
- Operations requiring strict ordering
- Single fast operation (overhead not worth it)

## Benefits

- **Performance**: Reduce total execution time dramatically
- **Throughput**: Process more items in less time
- **Resource Utilization**: Maximize worker and external service usage
- **Simplicity**: No manual thread management or synchronization
- **Reliability**: Temporal handles retries and failures per operation
- **Scalability**: Easily scale to hundreds of parallel operations

## Trade-offs

- **Resource Consumption**: More concurrent operations need more workers
- **Complexity**: Error handling across parallel operations is harder
- **Debugging**: Parallel execution makes tracing more difficult
- **Rate Limits**: May overwhelm external services without throttling
- **Memory**: Storing many promises consumes workflow memory

## How It Works

1. Workflow creates activity/child workflow stubs
2. `Async.function()` schedules operations and returns Promises immediately
3. Temporal dispatches operations to available workers concurrently
4. Each operation executes independently with its own retry logic
5. `Promise.allOf()` blocks until all operations complete
6. `Promise.get()` retrieves individual results
7. Workflow continues with collected results

## Comparison with Alternatives

| Approach | Parallelism | Complexity | Control | Use Case |
|----------|-------------|------------|---------|----------|
| Async.function() | High | Low | Medium | Independent operations |
| Sequential | None | Very Low | Full | Dependent operations |
| Child Workflows | High | Medium | High | Complex sub-processes |
| ContinueAsNew | None | Medium | Full | Large iterations |

## Related Patterns

- **Batch Processing**: Processing large datasets efficiently
- **Fan-Out/Fan-In**: Distribute work and aggregate results
- **Dynamic Workflows**: Variable number of parallel operations
- **Saga Pattern**: Parallel operations with compensation

## Sample Code

- [HelloParallelActivity](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/hello/HelloParallelActivity.java) - Basic parallel activity execution
- [HelloAsync](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/hello/HelloAsync.java) - Async execution with Promises
- [Sliding Window Batch](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/batch/slidingwindow) - Controlled parallel child workflows

## Best Practices

1. **Limit Concurrency**: Use batching to avoid overwhelming workers or external services
2. **Handle Failures**: Wrap operations in try-catch or use activity retry policies
3. **Set Timeouts**: Configure appropriate activity timeouts for parallel operations
4. **Monitor Resources**: Ensure sufficient workers for desired parallelism
5. **Aggregate Carefully**: Consider memory when collecting large result sets
6. **Use Child Workflows**: For complex parallel operations with their own state
7. **Test Scalability**: Verify performance with realistic parallel loads
8. **Rate Limiting**: Implement throttling for external API calls
9. **Partial Results**: Consider returning partial results on some failures
10. **Avoid Blocking**: Don't call `Promise.get()` until ready to wait for results
