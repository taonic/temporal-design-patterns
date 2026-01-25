# Approval Pattern

## Overview

The Approval pattern implements human-in-the-loop workflows where execution blocks until an external decision is made. It uses workflow signals with custom input data to unblock workflows, enabling approval processes, manual reviews, and decision gates in automated business processes.

## Problem

In business processes, you often need workflows that:
- Wait for human approval before proceeding
- Capture approval decisions with metadata (approver, reason, timestamp)
- Support approval, rejection, or escalation actions
- Handle timeout scenarios when approvals aren't received
- Track approval history and audit trails

Without proper approval patterns, you must:
- Poll external systems for approval status
- Implement complex state machines manually
- Risk losing approval context and metadata
- Handle race conditions between timeouts and approvals
- Build custom audit logging for compliance

## Solution

The Approval pattern uses `Workflow.await()` to block execution until a signal is received. Signals carry custom data (approval decision, approver details, comments) that the workflow captures and uses to determine next steps.

```java
public class ApprovalData {
  private String approver;
  private String decision; // "APPROVED", "REJECTED", "ESCALATED"
  private String comments;
  private long timestamp;
  
  // Constructor, getters, setters
}

@WorkflowInterface
public interface ApprovalWorkflow {
  @WorkflowMethod
  String execute(String requestId, Duration timeout);
  
  @SignalMethod
  void submitApproval(ApprovalData approvalData);
  
  @QueryMethod
  String getStatus();
}

public class ApprovalWorkflowImpl implements ApprovalWorkflow {
  private ApprovalData approvalData;
  private String status = "PENDING";
  
  @Override
  public String execute(String requestId, Duration timeout) {
    // Wait for approval signal or timeout
    boolean approved = Workflow.await(timeout, () -> approvalData != null);
    
    if (approved) {
      status = approvalData.getDecision();
      return "Request " + requestId + " " + status + " by " + approvalData.getApprover();
    } else {
      status = "TIMEOUT";
      return "Request " + requestId + " timed out";
    }
  }
  
  @Override
  public void submitApproval(ApprovalData data) {
    this.approvalData = data;
  }
  
  @Override
  public String getStatus() {
    return status;
  }
}
```

## Implementation

### Basic Approval with Timeout

```java
public class SimpleApprovalWorkflowImpl implements ApprovalWorkflow {
  private boolean approved = false;
  private String approver;
  
  @Override
  public String execute(String requestId, Duration timeout) {
    Workflow.await(timeout, () -> approved);
    
    if (approved) {
      return "Approved by " + approver;
    } else {
      return "Approval timeout - auto-rejected";
    }
  }
  
  @Override
  public void approve(String approverName) {
    this.approved = true;
    this.approver = approverName;
  }
}
```

### Multi-Level Approval Chain

```java
public class MultiLevelApprovalData {
  private String level; // "L1", "L2", "L3"
  private String approver;
  private String decision;
  private String comments;
}

public class MultiLevelApprovalWorkflowImpl implements ApprovalWorkflow {
  private List<MultiLevelApprovalData> approvals = new ArrayList<>();
  private String[] requiredLevels = {"L1", "L2", "L3"};
  
  @Override
  public String execute(String requestId, Duration timeoutPerLevel) {
    for (String level : requiredLevels) {
      // Wait for approval at this level
      boolean received = Workflow.await(
          timeoutPerLevel,
          () -> hasApprovalForLevel(level));
      
      if (!received) {
        return "Timeout at " + level;
      }
      
      MultiLevelApprovalData approval = getApprovalForLevel(level);
      if (approval.getDecision().equals("REJECTED")) {
        return "Rejected at " + level + " by " + approval.getApprover();
      }
    }
    
    return "Fully approved through all levels";
  }
  
  @Override
  public void submitApproval(MultiLevelApprovalData data) {
    approvals.add(data);
  }
  
  private boolean hasApprovalForLevel(String level) {
    return approvals.stream().anyMatch(a -> a.getLevel().equals(level));
  }
  
  private MultiLevelApprovalData getApprovalForLevel(String level) {
    return approvals.stream()
        .filter(a -> a.getLevel().equals(level))
        .findFirst()
        .orElse(null);
  }
}
```

### Approval with Escalation

```java
public class EscalatingApprovalWorkflowImpl implements ApprovalWorkflow {
  private ApprovalData approvalData;
  private boolean escalated = false;
  
  @Override
  public String execute(String requestId, Duration initialTimeout) {
    // Wait for initial approval
    boolean received = Workflow.await(initialTimeout, () -> approvalData != null);
    
    if (!received) {
      // Escalate to manager
      escalated = true;
      sendEscalationNotification();
      
      // Wait for escalated approval with extended timeout
      received = Workflow.await(
          Duration.ofHours(24),
          () -> approvalData != null);
      
      if (!received) {
        return "Escalation timeout - auto-rejected";
      }
    }
    
    String decision = approvalData.getDecision();
    String approver = approvalData.getApprover();
    String escalationNote = escalated ? " (escalated)" : "";
    
    return decision + " by " + approver + escalationNote;
  }
  
  @Override
  public void submitApproval(ApprovalData data) {
    this.approvalData = data;
  }
  
  private void sendEscalationNotification() {
    // Execute activity to send notification
    ActivityOptions options = ActivityOptions.newBuilder()
        .setStartToCloseTimeout(Duration.ofSeconds(10))
        .build();
    NotificationActivities activities = 
        Workflow.newActivityStub(NotificationActivities.class, options);
    activities.sendEscalationEmail();
  }
}
```

## Key Components

1. **Workflow.await()**: Blocks execution until signal received or timeout
2. **Signal Method**: Receives approval data from external systems
3. **Approval Data**: Custom object carrying decision, approver, comments, metadata
4. **Timeout Duration**: Maximum wait time before auto-rejection or escalation
5. **Query Methods**: Expose current approval status for monitoring
6. **Condition Lambda**: Checks if approval data has been received

## When to Use

**Ideal for:**
- Purchase order approvals
- Expense report reviews
- Code deployment gates
- Contract signing workflows
- Manual quality checks
- Compliance reviews
- Budget authorization
- Access request approvals

**Not ideal for:**
- Fully automated processes (no human needed)
- Real-time decisions (use synchronous APIs)
- Simple yes/no without context (use boolean signal)
- Processes requiring immediate response (< 1 second)

## Benefits

- **Rich Context**: Capture approver identity, reasons, timestamps
- **Audit Trail**: All approval data recorded in workflow history
- **Timeout Handling**: Automatic fallback when approvals aren't received
- **Flexible Logic**: Support multi-level, conditional, escalating approvals
- **Query Support**: Check approval status without modifying state
- **Deterministic**: Replay-safe with all decisions in history
- **Scalable**: Handles thousands of concurrent approval workflows

## Trade-offs

- **Signal-Based**: Requires external system to send approval signals
- **Blocking**: Workflow execution paused until approval received
- **Timeout Required**: Must define maximum wait time
- **No Built-in UI**: Need separate approval interface/system
- **History Size**: Large approval data increases history size

## How It Works

1. Workflow starts and reaches approval gate
2. Calls `Workflow.await(timeout, () -> approvalData != null)`
3. Workflow blocks, waiting for signal
4. External system sends approval signal with data
5. Signal handler sets `approvalData` field
6. Await condition becomes true, workflow unblocks
7. Workflow examines approval data and proceeds accordingly
8. If timeout expires before signal: workflow continues with timeout logic

## Comparison with Alternatives

| Approach | Rich Data | Timeout | Complexity | Use Case |
|----------|-----------|---------|------------|----------|
| Signal with Data | Yes | Yes | Low | Approval workflows |
| Update | Yes | No | Medium | Synchronous validation |
| Boolean Signal | No | Yes | Low | Simple yes/no |
| Polling Activity | Yes | Yes | High | External approval systems |

## Related Patterns

- **Signal-Based Event Handling**: Receiving external events
- **Updatable Timer**: Extending approval deadlines dynamically
- **Query for State Inspection**: Checking approval status
- **Human-in-the-Loop**: Manual intervention in automated processes
- **Saga Pattern**: Compensating actions on rejection

## Sample Code

- [Hello Signal](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/hello/HelloSignal.java) - Basic signal handling
- [Safe Message Passing](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/safemessagepassing) - Concurrent signal handling

## Best Practices

1. **Use Custom Data Objects**: Capture rich approval context, not just boolean
2. **Set Reasonable Timeouts**: Balance responsiveness with approval time needs
3. **Add Query Methods**: Enable status checking without signals
4. **Validate Signal Data**: Check approver permissions, data completeness
5. **Log Approval Events**: Record decisions for audit trails
6. **Handle Timeouts Gracefully**: Define clear timeout behavior (reject, escalate, notify)
7. **Support Cancellation**: Allow workflows to be cancelled if request withdrawn
8. **Add Idempotency**: Handle duplicate approval signals safely
9. **Include Timestamps**: Record when approval was submitted
10. **Expose Approval History**: Query method to retrieve all approval attempts

## Common Pitfalls

1. **No Timeout**: Workflow waits indefinitely for approval
2. **Missing Validation**: Accepting approvals from unauthorized users
3. **Lost Context**: Not capturing approver identity or reason
4. **Race Conditions**: Not handling signal arriving during timeout
5. **No Audit Trail**: Not logging approval decisions
6. **Tight Timeouts**: Timeout too short for realistic approval time
7. **Boolean Only**: Using simple boolean instead of rich data object
8. **No Status Query**: Can't check approval status externally
9. **Duplicate Handling**: Not managing multiple approval signals
10. **No Escalation Path**: No fallback when initial approval times out
