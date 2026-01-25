# Polling External Services

## Overview

The Polling External Services pattern implements strategies for periodically checking external systems until a desired state is reached. It enables workflows to wait for asynchronous operations in third-party services that don't support callbacks, making it essential for integrating with REST APIs, job queues, and batch processing systems.

## Problem

In distributed systems, you often need workflows that:
- Wait for external jobs to complete (batch processing, data pipelines)
- Poll REST APIs that don't provide webhooks
- Check status of long-running operations in third-party systems
- Handle varying poll frequencies (seconds vs minutes)
- Avoid overwhelming external services with requests

Without proper polling strategies, you must:
- Implement complex retry logic manually
- Risk unbounded workflow history growth
- Choose between responsiveness and resource efficiency
- Handle heartbeating and timeout management yourself

## Solution

You can use Temporal to implement three distinct polling strategies, each optimized for different polling frequencies and requirements:

1. **Frequent Polling (≤1 second)**: Loop inside activity with heartbeats
2. **Infrequent Polling (≥1 minute)**: Use activity retries with fixed backoff
3. **Periodic Sequence**: Use child workflows for complex polling sequences

## Implementation

### 1. Frequent Polling (Fast Response Required)

For polling intervals of 1 second or faster, implement the polling loop inside the activity with heartbeats.

```java
@ActivityInterface
public interface PollingActivities {
  String doPoll();
}

public class FrequentPollingActivityImpl implements PollingActivities {
  @Override
  public String doPoll() {
    while (true) {
      // Heartbeat to report progress and enable timely restarts
      Activity.getExecutionContext().heartbeat(null);
      
      // Poll the external service
      String result = externalService.checkStatus();
      
      if (result.equals("COMPLETED")) {
        return result;
      }
      
      // Sleep before next poll (1 second)
      try {
        Thread.sleep(1000);
      } catch (InterruptedException e) {
        throw Activity.wrap(e);
      }
    }
  }
}

public class FrequentPollingWorkflowImpl implements PollingWorkflow {
  @Override
  public String exec() {
    ActivityOptions options = ActivityOptions.newBuilder()
        .setStartToCloseTimeout(Duration.ofSeconds(60))
        .setHeartbeatTimeout(Duration.ofSeconds(2)) // Must be < StartToClose
        .build();
    
    PollingActivities activities = Workflow.newActivityStub(PollingActivities.class, options);
    return activities.doPoll();
  }
}
```

### 2. Infrequent Polling (Resource Efficient)

For polling intervals of 1 minute or slower, use activity retries with a backoff coefficient of 1.

```java
public class InfrequentPollingActivityImpl implements PollingActivities {
  @Override
  public String doPoll() {
    String result = externalService.checkStatus();
    
    if (!result.equals("COMPLETED")) {
      // Throw to trigger retry after interval
      throw new RuntimeException("Service not ready, will retry");
    }
    
    return result;
  }
}

public class InfrequentPollingWorkflowImpl implements PollingWorkflow {
  @Override
  public String exec() {
    ActivityOptions options = ActivityOptions.newBuilder()
        .setStartToCloseTimeout(Duration.ofSeconds(2))
        .setRetryOptions(
            RetryOptions.newBuilder()
                .setBackoffCoefficient(1) // Fixed interval
                .setInitialInterval(Duration.ofSeconds(60)) // Poll every 60s
                .build())
        .build();
    
    PollingActivities activities = Workflow.newActivityStub(PollingActivities.class, options);
    return activities.doPoll();
  }
}
```

### 3. Periodic Sequence (Complex Polling)

For polling that requires multiple activities or changing parameters between attempts, use child workflows with continue-as-new.

```java
@WorkflowInterface
public interface PollingChildWorkflow {
  @WorkflowMethod
  String exec(int pollingIntervalInSeconds);
}

public class PeriodicPollingChildWorkflowImpl implements PollingChildWorkflow {
  @Override
  public String exec(int pollingIntervalInSeconds) {
    ActivityOptions options = ActivityOptions.newBuilder()
        .setStartToCloseTimeout(Duration.ofSeconds(10))
        .build();
    
    PollingActivities activities = Workflow.newActivityStub(PollingActivities.class, options);
    
    int maxAttempts = 10;
    for (int i = 0; i < maxAttempts; i++) {
      String result = activities.doPoll();
      
      if (result.equals("COMPLETED")) {
        return result;
      }
      
      Workflow.sleep(Duration.ofSeconds(pollingIntervalInSeconds));
    }
    
    // Continue-as-new to prevent unbounded history
    PollingChildWorkflow continueAsNew = Workflow.newContinueAsNewStub(PollingChildWorkflow.class);
    continueAsNew.exec(pollingIntervalInSeconds);
    return null; // Unreachable
  }
}

public class PeriodicPollingWorkflowImpl implements PollingWorkflow {
  @Override
  public String exec() {
    PollingChildWorkflow childWorkflow = Workflow.newChildWorkflowStub(
        PollingChildWorkflow.class,
        ChildWorkflowOptions.newBuilder()
            .setWorkflowId("ChildWorkflowPoll")
            .build());
    
    return childWorkflow.exec(5); // Poll every 5 seconds
  }
}
```

## Key Components

### Frequent Polling
1. **Activity Loop**: Polling logic runs inside activity
2. **Heartbeats**: Report progress on each iteration
3. **HeartbeatTimeout**: Must be shorter than StartToCloseTimeout
4. **Thread.sleep()**: Delay between polls (activity code, not workflow)

### Infrequent Polling
1. **Activity Retries**: Each poll attempt is a separate activity execution
2. **BackoffCoefficient = 1**: Fixed retry interval
3. **InitialInterval**: Sets the polling frequency
4. **No History Growth**: Retries don't add to workflow history

### Periodic Sequence
1. **Child Workflow**: Encapsulates polling logic
2. **Continue-As-New**: Prevents unbounded history in long-running polls
3. **Activity Sequence**: Can execute multiple activities per poll
4. **Parent Unaware**: Parent doesn't see continue-as-new, only completion

## When to Use

### Frequent Polling (≤1 second)
**Ideal for:**
- Real-time status checks
- High-priority operations requiring fast response
- Short-lived external operations (minutes, not hours)
- Systems that can handle frequent requests

**Not ideal for:**
- Long-running operations (hours/days)
- Rate-limited APIs
- Resource-constrained external services

### Infrequent Polling (≥1 minute)
**Ideal for:**
- Batch job completion checks
- Long-running external processes
- Rate-limited APIs
- Operations that may take hours or days
- Minimizing workflow history size

**Not ideal for:**
- Sub-minute polling requirements
- Operations requiring immediate response
- Complex multi-step polling sequences

### Periodic Sequence
**Ideal for:**
- Multi-step polling sequences
- Changing activity parameters between polls
- Complex polling logic with state
- Very long-running polls requiring continue-as-new

**Not ideal for:**
- Simple single-activity polling
- When frequent or infrequent patterns suffice

## Benefits

- **No Callback Required**: Works with any external service
- **Automatic Retries**: Built-in retry handling
- **Deterministic**: All timing based on workflow time
- **Scalable**: Efficient resource usage based on polling frequency
- **Fault Tolerant**: Survives worker restarts and failures
- **History Efficient**: Infrequent polling doesn't bloat history

## Trade-offs

### Frequent Polling
- **Pros**: Fast response, simple implementation
- **Cons**: Higher resource usage, activity must heartbeat, limited to shorter operations

### Infrequent Polling
- **Pros**: Minimal history growth, efficient for long operations, simple
- **Cons**: Minimum 1-minute intervals, single activity only

### Periodic Sequence
- **Pros**: Flexible, supports complex sequences, unbounded duration
- **Cons**: More complex, requires child workflow management

## How It Works

### Frequent Polling Flow
1. Workflow starts activity with heartbeat timeout
2. Activity enters polling loop
3. On each iteration: heartbeat → poll → check result → sleep
4. If complete: return result
5. If heartbeat timeout: activity restarts from beginning
6. Workflow receives result when polling succeeds

### Infrequent Polling Flow
1. Workflow starts activity with retry policy
2. Activity polls external service
3. If not ready: throw exception
4. Temporal waits for InitialInterval (e.g., 60s)
5. Activity retries (not recorded in history)
6. Repeat until success or max attempts
7. Workflow receives result when polling succeeds

### Periodic Sequence Flow
1. Parent workflow starts child workflow
2. Child workflow loops: poll → check → sleep
3. After N iterations: child calls continue-as-new
4. New child run continues polling
5. Parent remains blocked, unaware of continue-as-new
6. When complete: child returns result to parent

## Comparison with Alternatives

| Strategy | Poll Frequency | History Impact | Complexity | Best For |
|----------|---------------|----------------|------------|----------|
| Frequent Polling | ≤1 second | Medium | Low | Real-time checks |
| Infrequent Polling | ≥1 minute | Minimal | Low | Long operations |
| Periodic Sequence | Any | Low (with CAN) | Medium | Complex sequences |
| Workflow Timer Loop | Any | High | Medium | Simple cases only |

## Related Patterns

- **Async Activity Completion**: When external service can callback
- **Heartbeating Activity**: Reporting progress in long activities
- **Continue-As-New**: Managing unbounded workflow history
- **Retry Strategies**: Configuring activity retry behavior

## Sample Code

- [Frequent Polling](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/polling/frequent) - Fast polling with heartbeats
- [Infrequent Polling](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/polling/infrequent) - Efficient long-interval polling
- [Periodic Sequence](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/polling/periodicsequence) - Complex polling with child workflows

## Best Practices

1. **Choose the Right Strategy**: Match polling frequency to the pattern
2. **Set Appropriate Timeouts**: HeartbeatTimeout < StartToCloseTimeout for frequent polling
3. **Handle Failures Gracefully**: Distinguish transient from permanent failures
4. **Add Exponential Backoff**: For error cases (not normal polling)
5. **Implement Circuit Breakers**: Protect external services from overload
6. **Use Continue-As-New**: For very long-running polls (periodic sequence)
7. **Monitor Polling Metrics**: Track poll attempts, success rates, durations
8. **Respect Rate Limits**: Adjust polling frequency to API constraints
9. **Add Jitter**: Prevent thundering herd when many workflows poll simultaneously
10. **Consider Webhooks**: If external service supports callbacks, use async completion instead

## Common Pitfalls

1. **Wrong Pattern Choice**: Using frequent polling for hour-long operations
2. **Missing Heartbeats**: Frequent polling without heartbeats causes delayed restarts
3. **Unbounded History**: Not using continue-as-new in periodic sequence
4. **Tight Polling Loops**: Polling too frequently overwhelms external services
5. **No Timeout**: Polling indefinitely without max attempts or deadline
6. **Ignoring Errors**: Not distinguishing between retryable and permanent failures
7. **Workflow Timer Loops**: Using workflow timers instead of proper polling patterns
