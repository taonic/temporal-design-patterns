
# Delayed Start Pattern

## Overview

The Delayed Start pattern enables Workflows to be created immediately but begin execution after a specified delay.
The Workflow execution is registered in Temporal right away, but the first Workflow Task is scheduled to run only after the delay period expires, making it suitable for scheduled operations, grace periods, and deferred processing.

## Problem

In business processes, you often need Workflows that start execution at a future time, are created immediately for tracking but execute later, avoid external scheduling systems or cron jobs for one-time delays, and maintain Workflow identity and queryability before execution begins.

Without delayed start, you must use external schedulers to trigger Workflow creation later, start Workflows immediately and sleep as the first operation (which wastes resources), implement complex queueing systems for deferred execution, or use Temporal Schedules for one-time delays (which is more than you need).

## Solution

The Delayed Start uses `setStartDelay()` in WorkflowOptions to defer the first Workflow Task.
The Workflow execution is created immediately with a `firstWorkflowTaskBackoff` set to the delay duration, but no Workflow code runs until the delay expires.

```mermaid
sequenceDiagram
    participant Client
    participant Temporal
    participant Workflow

    Client->>Temporal: Start with setStartDelay(30s)
    Temporal->>Temporal: Create execution
    Note over Temporal: Execution visible<br/>but not running
    Temporal-->>Client: Workflow ID
    
    Note over Temporal: Delay period (30s)...
    
    opt During delay
        Client->>Temporal: Signal-With-Start
        Note over Temporal: Bypasses remaining delay
    end
    
    Note over Temporal: Delay expires (if not bypassed)
    Temporal->>+Workflow: Schedule first task
    Workflow->>Workflow: Execute
    Workflow-->>-Temporal: Complete
```

The following describes each step in the diagram:

1. The client starts the Workflow with a 30-second delay. Temporal creates the execution immediately.
2. The execution is visible and queryable, but no Workflow code runs during the delay.
3. If the client sends a Signal-With-Start or Update-With-Start during the delay, the remaining delay is bypassed and a Workflow Task is dispatched immediately. Regular Signals do not interrupt the delay.
4. After the delay expires, Temporal schedules the first Workflow Task and the Workflow begins execution.

The following example creates a Workflow with a 30-second start delay:

```java
// Client.java
DelayedStartWorkflow workflow = client.newWorkflowStub(
    DelayedStartWorkflow.class,
    WorkflowOptions.newBuilder()
        .setWorkflowId(WORKFLOW_ID)
        .setTaskQueue(TASK_QUEUE)
        .setStartDelay(Duration.ofSeconds(30))
        .build());

workflow.start(); // Created now, executes in 30 seconds
```

The `setStartDelay()` method sets the `firstWorkflowTaskBackoff` on the execution.
The Workflow is created and visible in the UI immediately, but the Worker does not receive a Task until the delay expires.

## Implementation

### Basic delayed notification

The following implementation sends a notification after a one-hour delay.
The Workflow code runs only after the delay expires:

```java
// NotificationWorkflowImpl.java
@WorkflowInterface
public interface NotificationWorkflow {
  @WorkflowMethod
  void sendNotification(String message);
}

public class NotificationWorkflowImpl implements NotificationWorkflow {
  @Override
  public void sendNotification(String message) {
    Workflow.getLogger(NotificationWorkflowImpl.class)
        .info("Sending notification: " + message);
  }
}

// Client.java
NotificationWorkflow workflow = client.newWorkflowStub(
    NotificationWorkflow.class,
    WorkflowOptions.newBuilder()
        .setTaskQueue(TASK_QUEUE)
        .setStartDelay(Duration.ofHours(1))
        .build());

workflow.sendNotification("Your trial expires soon");
```

The Workflow is created immediately, but the `sendNotification` method does not execute until one hour later.

### Cancellable delayed execution

The following implementation adds Signal handlers for cancellation and a Query for status.
You can cancel the Workflow before it runs or check its status during the delay:

```java
// DelayedOrderWorkflowImpl.java
@WorkflowInterface
public interface DelayedOrderWorkflow {
  @WorkflowMethod
  void processOrder(String orderId);
  
  @SignalMethod
  void cancel();
  
  @QueryMethod
  String getStatus();
}

public class DelayedOrderWorkflowImpl implements DelayedOrderWorkflow {
  private boolean cancelled = false;
  private String status = "SCHEDULED";
  
  @Override
  public void processOrder(String orderId) {
    if (cancelled) {
      status = "CANCELLED";
      return;
    }
    
    status = "PROCESSING";
    // Process order logic
    status = "COMPLETED";
  }
  
  @Override
  public void cancel() {
    cancelled = true;
  }
  
  @Override
  public String getStatus() {
    return status;
  }
}
```

The `cancel` Signal handler sets a flag that the Workflow checks when it starts executing.
Note that Signal handlers and Query handlers only run after the delay expires and the first Workflow Task is dispatched.
To cancel before execution, use `Signal-With-Start` to bypass the delay, or cancel the Workflow Execution directly.

## When to use

The Delayed Start pattern is a good fit for scheduled one-time operations (send a reminder in 24 hours), grace periods before processing (cancel a subscription in 7 days), delayed notifications and alerts, deferred batch processing, and trial expiration Workflows.

It is not a good fit for recurring Schedules (use Temporal Schedules), immediate execution with internal delays (use `Workflow.sleep()`), complex scheduling logic (use Schedules with cron), or sub-second delays (minimal benefit).

## Benefits and trade-offs

The Workflow is queryable before execution starts (immediate visibility).
No Worker resources are consumed during the delay.
You can cancel the Workflow Execution before it runs.
A Signal-With-Start or Update-With-Start bypasses the remaining delay.
Regular Signals sent during the delay do not interrupt it.
The API is a single configuration option with no external schedulers needed.
The delay is managed by Temporal, ensuring deterministic behavior.

The trade-offs to consider are that you cannot dynamically adjust the delay after creation (use the Updatable Timer pattern for that).
The pattern is for one-time delays only — for recurring Schedules, use Temporal Schedules.
Very short delays (milliseconds) provide minimal benefit — the minimum timer duration is 1 second.
The delay is time-based only, not condition-based.
Regular Signals sent during the delay are not delivered until the first Workflow Task fires, so Query and Signal handlers are not available until execution begins.

## Comparison with alternatives

| Approach | Immediate visibility | Resource usage | Cancellable | Use case |
| :--- | :--- | :--- | :--- | :--- |
| Delayed Start | Yes | None during delay | Yes | One-time future execution |
| Workflow.sleep() | Yes | Worker resources | Yes | Internal delays |
| Temporal Schedules | Yes | None | Yes | Recurring Schedules |
| External Scheduler | No | External system | Depends | Complex scheduling |

## Best practices

- **Use for one-time delays.** For recurring Schedules, use Temporal Schedules instead.
- **Set Workflow ID.** Always set an explicit Workflow ID for tracking and cancellation.
- **Add Query methods.** Expose status via Queries to check state during the delay.
- **Enable cancellation.** Add Signal handlers to cancel before execution.
- **Validate delay duration.** Ensure the delay is reasonable (not too short or too long).
- **Monitor backoff.** Check `firstWorkflowTaskBackoff` in history for verification.
- **Consider time zones.** Use absolute timestamps if the delay depends on a specific time.
- **Document behavior.** Clearly indicate that the Workflow does not execute immediately.

## Common pitfalls

- **Using Signals during the delay.** Regular Signals do not interrupt the Start Delay. Only Signal-With-Start or Update-With-Start bypass the delay. Signals sent to a delayed Workflow are buffered but the Workflow code has not started, so there is no handler to process them until the delay expires.
- **Querying before the Workflow starts.** Queries have no state to return during the delay because no Workflow code has executed yet. Clients may receive errors or empty results.
- **Setting delays shorter than 1 second.** The minimum timer resolution is 1 second. Sub-second delays are not supported.
- **Forgetting that the Workflow ID is reserved.** A delayed Workflow reserves its Workflow ID immediately. Starting another Workflow with the same ID will fail depending on the ID reuse policy.

## Related patterns

- **Temporal Schedules**: For recurring Workflow execution.
- **[Updatable Timer](updatable-timer.md)**: For dynamically adjustable delays within Workflows.
- **[Signal with Start](signal-with-start.md)**: Interacting with Workflows before execution.

## Sample code

- [Full Java Sample](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/hello/HelloDelayedStart.java) — Complete implementation with delayed start.
