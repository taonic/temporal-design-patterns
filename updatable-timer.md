# Updatable Timer Pattern

## Overview

The Updatable Timer pattern implements a sleep operation that can be interrupted and dynamically adjusted via signals. It enables workflows to wait for deadlines that can be extended or shortened based on external events, making it ideal for approval processes, SLA management, and time-sensitive business operations.

## Problem

In business processes, you often need workflows that:
- Wait for a deadline (approval timeout, SLA expiration, grace period)
- Allow the deadline to be extended or shortened dynamically
- React immediately when the deadline changes
- Continue waiting with the new deadline without restarting

Without an updatable timer, you must:
- Use fixed timeouts that can't be adjusted
- Cancel and restart workflows to change deadlines
- Poll frequently to check for deadline changes
- Implement complex state machines to handle timing updates

## Solution

The Updatable Timer uses `Workflow.await()` with a time condition that can be modified via signals. When a signal updates the wake-up time, the await condition becomes true, the workflow recalculates the sleep duration, and blocks again with the new deadline.

```java
public class UpdatableTimer {
  private long wakeUpTime;
  private boolean wakeUpTimeUpdated;

  public void sleepUntil(long wakeUpTime) {
    this.wakeUpTime = wakeUpTime;
    while (true) {
      wakeUpTimeUpdated = false;
      Duration sleepInterval = Duration.ofMillis(this.wakeUpTime - Workflow.currentTimeMillis());
      if (!Workflow.await(sleepInterval, () -> wakeUpTimeUpdated)) {
        break; // Timer expired
      }
      // Timer was updated, loop to recalculate
    }
  }

  public void updateWakeUpTime(long wakeUpTime) {
    this.wakeUpTime = wakeUpTime;
    this.wakeUpTimeUpdated = true; // Unblocks await
  }
}
```

## Implementation

### Basic Approval Workflow

```java
@WorkflowInterface
public interface ApprovalWorkflow {
  @WorkflowMethod
  void execute(long approvalDeadline);
  
  @SignalMethod
  void extendDeadline(long newDeadline);
  
  @SignalMethod
  void approve();
  
  @QueryMethod
  String getStatus();
}

public class ApprovalWorkflowImpl implements ApprovalWorkflow {
  private UpdatableTimer timer = new UpdatableTimer();
  private boolean approved = false;
  private String status = "PENDING";
  
  @Override
  public void execute(long approvalDeadline) {
    // Wait for approval or deadline
    Workflow.await(
        Duration.ofMillis(approvalDeadline - Workflow.currentTimeMillis()),
        () -> approved);
    
    if (approved) {
      status = "APPROVED";
    } else {
      status = "REJECTED";
    }
  }
  
  @Override
  public void extendDeadline(long newDeadline) {
    timer.updateWakeUpTime(newDeadline);
  }
  
  @Override
  public void approve() {
    approved = true;
  }
  
  @Override
  public String getStatus() {
    return status;
  }
}
```

### Advanced: Multiple Deadline Extensions

```java
public class ApprovalWorkflowImpl implements ApprovalWorkflow {
  private UpdatableTimer timer = new UpdatableTimer();
  private boolean approved = false;
  private boolean rejected = false;
  
  @Override
  public void execute(long initialDeadline) {
    timer.sleepUntil(initialDeadline);
    
    // Check if approved during wait
    if (!approved) {
      rejected = true;
    }
  }
  
  @Override
  public void extendDeadline(long newDeadline) {
    if (!approved && !rejected) {
      timer.updateWakeUpTime(newDeadline);
    }
  }
  
  @Override
  public void approve() {
    approved = true;
  }
}
```

## Key Components

1. **UpdatableTimer**: Reusable helper class that implements the updatable sleep logic
2. **wakeUpTime**: Target timestamp when the timer should expire
3. **wakeUpTimeUpdated**: Flag that unblocks `Workflow.await()` when deadline changes
4. **Signal Handler**: Updates the wake-up time and sets the flag
5. **Workflow.await()**: Blocks with both time and condition—whichever comes first

## When to Use

**Ideal for:**
- Approval workflows with deadline extensions
- SLA management with grace periods
- Time-based escalations that can be postponed
- Auction bidding with extended closing times
- Payment grace periods that can be adjusted

**Not ideal for:**
- Fixed timeouts that never change (use simple `Workflow.sleep()`)
- Immediate cancellation (use cancellation scopes)
- Complex scheduling (use Temporal Schedules)

## Benefits

- **Dynamic Timing**: Adjust deadlines without restarting workflows
- **Immediate Response**: Changes take effect instantly
- **Reusable**: UpdatableTimer can be used across multiple workflows
- **Deterministic**: All timing is based on workflow time, ensuring replay consistency
- **Query Support**: Can query current deadline at any time

## Trade-offs

- **Signal-Based**: Requires external process to send update signals
- **Single Timer**: Each UpdatableTimer instance manages one deadline
- **No History**: Previous deadlines aren't tracked (add if needed)
- **Manual Calculation**: Must calculate absolute timestamps (not relative durations)

## How It Works

1. Workflow calls `timer.sleepUntil(deadline)`
2. Timer calculates sleep duration and calls `Workflow.await(duration, () -> updated)`
3. Await blocks until either:
   - Duration expires → timer completes
   - Condition becomes true → signal updated the deadline
4. If condition triggered, loop recalculates duration and awaits again
5. If duration expired, timer completes and workflow continues

## Comparison with Alternatives

| Approach | Dynamic Updates | Complexity | Use Case |
|----------|----------------|------------|----------|
| Updatable Timer | Yes | Medium | Adjustable deadlines |
| Workflow.sleep() | No | Low | Fixed delays |
| Cancellation Scope | Yes (cancel only) | Medium | Abort operations |
| Polling Loop | Yes | High | Frequent checks |

## Related Patterns

- **Signal-Based Event Handling**: Receiving external events to modify behavior
- **Workflow Timers**: Using explicit timers for timeout control
- **Cancellation Scopes**: Canceling operations when conditions change
- **Query for State Inspection**: Checking current deadline status

## Sample Code

- [Full Java Sample](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/updatabletimer) - Complete implementation with starter and updater

## Best Practices

1. **Use Absolute Timestamps**: Store wake-up time as epoch millis, not relative durations
2. **Validate Updates**: Ensure new deadlines are in the future
3. **Add Queries**: Expose current deadline via query methods
4. **Handle Edge Cases**: Check if timer already expired before updating
5. **Consider Max Extensions**: Limit how many times or how far deadlines can be extended
6. **Log Changes**: Log each deadline update for observability
7. **Reuse UpdatableTimer**: Extract to helper class for use across workflows
8. **Combine with Conditions**: Use `Workflow.await()` with both time and business conditions
