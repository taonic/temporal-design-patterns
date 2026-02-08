---
layout: default
title: Child Workflows
parent: Stateful / Lifecycle Patterns
nav_order: 2
---

# Child Workflows Pattern

## Overview

Child Workflows enable decomposition of complex business logic into smaller, reusable workflow units. Each child executes as an independent workflow with its own workflow ID, event history (50K event limit), and lifecycle. Unlike activities which execute code, child workflows orchestrate processes and provide workflow-level semantics: independent tracking, querying, timeouts, and the ability to outlive the parent.

Key capabilities:
- **Independent Identity**: Each child has a unique workflow ID visible in the UI for tracking and querying
- **Separate History**: Each child maintains its own event history, preventing parent history bloat
- **Flexible Invocation**: Synchronous (blocking) or asynchronous (non-blocking) execution
- **Lifecycle Control**: Parent close policies (TERMINATE, ABANDON, REQUEST_CANCEL) determine child behavior when parent completes
- **Task Queue Routing**: Children can execute on different task queues with specialized workers
- **Reusability**: Same child workflow logic can be invoked by multiple different parent workflows

## Problem

In distributed systems, you often need workflows that:
- Break down complex processes into modular, reusable components
- Execute sub-processes that may outlive the parent workflow
- Coordinate multiple independent workflows with different lifecycles
- Isolate failure domains while maintaining orchestration control
- Reuse workflow logic across different parent workflows

Without child workflows, you must:
- Implement all logic in a single monolithic workflow
- Manually coordinate separate workflows via signals and queries
- Duplicate workflow logic across multiple implementations
- Manage complex state machines for sub-process coordination

## Solution

Child Workflows are invoked from parent workflows using `Workflow.newChildWorkflowStub()`. They can be called synchronously (blocking until completion) or asynchronously (fire-and-forget). The `ParentClosePolicy` determines what happens to children when the parent completes.

### Synchronous Child Workflow

```java
@WorkflowInterface
public interface ParentWorkflow {
  @WorkflowMethod
  String execute(String input);
}

public class ParentWorkflowImpl implements ParentWorkflow {
  @Override
  public String execute(String input) {
    // Create child workflow stub
    ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class);
    
    // Synchronous call - blocks until child completes
    String result = child.processData(input);
    
    return "Parent received: " + result;
  }
}
```

### Asynchronous Child Workflow

```java
public class ParentWorkflowImpl implements ParentWorkflow {
  @Override
  public WorkflowExecution execute(String input) {
    ChildWorkflowOptions options = ChildWorkflowOptions.newBuilder()
        .setWorkflowId("child-" + Workflow.randomUUID())
        .setParentClosePolicy(ParentClosePolicy.PARENT_CLOSE_POLICY_ABANDON)
        .build();
    
    ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class, options);
    
    // Async call - returns immediately
    Async.function(child::processData, input);
    
    // Get child execution info without waiting for completion
    Promise<WorkflowExecution> childExecution = Workflow.getWorkflowExecution(child);
    return childExecution.get(); // Blocks only until child starts
  }
}
```

## Parent Close Policy

The `ParentClosePolicy` determines child workflow behavior when the parent closes:

| Policy | Behavior | Use Case |
|--------|----------|----------|
| `TERMINATE` | Child is terminated when parent closes | Tightly coupled processes |
| `ABANDON` | Child continues independently | Fire-and-forget, long-running tasks |
| `REQUEST_CANCEL` | Child receives cancellation request | Graceful cleanup |

### Example: Abandon Policy

```java
ChildWorkflowOptions options = ChildWorkflowOptions.newBuilder()
    .setParentClosePolicy(ParentClosePolicy.PARENT_CLOSE_POLICY_ABANDON)
    .build();

ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class, options);
Async.function(child::longRunningTask);

// Parent can complete while child continues
return "Parent done, child continues";
```

## Synchronous vs Asynchronous Invocation

### Synchronous (Blocking)

```java
// Direct call - blocks until child completes
ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class);
String result = child.process(data); // Waits for completion
```

**Characteristics:**
- Parent waits for child to complete
- Child result is returned directly
- Parent history includes child completion
- Simpler error handling
- Child must complete before parent can proceed

### Asynchronous (Non-Blocking)

```java
// Async call - returns immediately
ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class);
Promise<String> result = Async.function(child::process, data);

// Do other work
doOtherWork();

// Optionally wait for result later
String value = result.get();
```

**Characteristics:**
- Parent continues immediately
- Returns `Promise<T>` for later retrieval
- Can start multiple children in parallel
- Parent can complete before child (with ABANDON policy)
- More flexible orchestration

## Implementation Patterns

### Pattern 1: Parallel Child Workflows

```java
public class ParentWorkflowImpl implements ParentWorkflow {
  @Override
  public String execute(List<String> items) {
    List<Promise<String>> promises = new ArrayList<>();
    
    for (String item : items) {
      ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class);
      promises.add(Async.function(child::process, item));
    }
    
    // Wait for all children to complete
    Promise.allOf(promises).get();
    
    // Collect results
    return promises.stream()
        .map(Promise::get)
        .collect(Collectors.joining(", "));
  }
}
```

### Pattern 2: Fire-and-Forget

```java
public class ParentWorkflowImpl implements ParentWorkflow {
  @Override
  public void execute(String data) {
    ChildWorkflowOptions options = ChildWorkflowOptions.newBuilder()
        .setParentClosePolicy(ParentClosePolicy.PARENT_CLOSE_POLICY_ABANDON)
        .build();
    
    ChildWorkflow child = Workflow.newChildWorkflowStub(ChildWorkflow.class, options);
    
    // Start child and don't wait
    Async.function(child::longRunningProcess, data);
    
    // Parent completes immediately, child continues
  }
}
```

### Pattern 3: Conditional Child Execution

```java
public class ParentWorkflowImpl implements ParentWorkflow {
  @Override
  public String execute(Order order) {
    if (order.requiresApproval()) {
      ApprovalWorkflow approval = Workflow.newChildWorkflowStub(ApprovalWorkflow.class);
      boolean approved = approval.requestApproval(order);
      
      if (!approved) {
        return "Order rejected";
      }
    }
    
    FulfillmentWorkflow fulfillment = Workflow.newChildWorkflowStub(FulfillmentWorkflow.class);
    return fulfillment.fulfill(order);
  }
}
```

## Key Components

1. **Child Workflow Stub**: Created via `Workflow.newChildWorkflowStub()`
2. **ChildWorkflowOptions**: Configures workflow ID, task queue, timeouts, parent close policy
3. **Async.function()**: Invokes child asynchronously, returns `Promise<T>`
4. **Workflow.getWorkflowExecution()**: Gets child execution info without waiting for completion
5. **ParentClosePolicy**: Controls child lifecycle when parent closes

## When to Use Child Workflows vs Activities

Child workflows and activities serve different purposes. Understanding when to use each is critical for effective workflow design.

### Use Child Workflows When:

1. **You need a separate workflow ID for tracking and querying**
   - Each child has its own workflow ID visible in the UI
   - Can query child workflow state independently
   - Enables business-level tracking (e.g., per-order, per-customer workflows)

2. **The operation may outlive the parent workflow**
   - Long-running processes that continue after parent completes
   - Fire-and-forget operations with ABANDON policy
   - Independent lifecycle management

3. **You need to reuse workflow logic across multiple parents**
   - Common sub-processes used by different workflows
   - Standardized business operations (approval, fulfillment, notification)
   - Shared workflow implementations

4. **You want to execute workflows on different task queues**
   - Route child to specialized workers
   - Separate resource pools or worker capabilities
   - Different deployment or scaling requirements

5. **You need independent history and event limits**
   - Each child has its own 50K event history limit
   - Prevents parent history from growing unbounded
   - Isolates complex sub-processes

6. **You want to apply different timeouts or retry policies at the workflow level**
   - Child workflows have their own execution timeouts
   - Independent retry and failure handling
   - Different SLAs for sub-processes

### Use Activities When:

- Executing external operations (API calls, database queries)
- Simple, short-lived operations
- No need for independent workflow tracking
- Tightly coupled to parent workflow lifecycle
- Lower overhead is important

### Key Distinction

**Activities** are for executing code (especially external operations).
**Child Workflows** are for orchestrating processes that benefit from independent workflow semantics.

## Benefits

- **Modularity**: Break complex logic into reusable units
- **Independent Workflow ID**: Each child is a first-class workflow with its own ID for tracking
- **Independent History**: Each child has its own 50K event history limit
- **Flexible Lifecycle**: Children can outlive parents with ABANDON policy
- **Parallel Execution**: Start multiple children concurrently
- **Failure Isolation**: Child failures don't automatically fail parent
- **Reusability**: Same child workflow used by multiple parents
- **Task Queue Routing**: Route children to different worker pools
- **Independent Timeouts**: Each child has its own execution timeout configuration

## Trade-offs

- **Overhead**: Each child is a separate workflow execution with its own history
- **Complexity**: More moving parts than single workflow
- **Visibility**: Child execution details not in parent history (but queryable independently)
- **Coordination**: Async children require explicit synchronization if needed
- **Cost**: More workflow executions = higher resource usage
- **Latency**: Starting a child workflow has more overhead than starting an activity
- **Event Count**: Parent history includes ChildWorkflowExecutionStarted/Completed events

## How It Works

### Synchronous Flow
1. Parent creates child workflow stub
2. Parent calls child method directly
3. Child workflow starts and executes
4. Parent blocks until child completes
5. Child result returned to parent
6. Parent continues with result

### Asynchronous Flow
1. Parent creates child workflow stub with options
2. Parent calls `Async.function(child::method)`
3. Child workflow starts asynchronously
4. Parent receives `Promise<T>` immediately
5. Parent can continue or wait on promise later
6. If ABANDON policy, parent can complete before child

## Comparison with Alternatives

| Approach | Modularity | Independent History | Can Outlive Parent | Overhead | Separate Workflow ID |
|----------|------------|---------------------|-------------------|----------|---------------------|
| Child Workflow | High | Yes | Yes (ABANDON) | Medium | Yes |
| Activity | Medium | No | No | Low | No |
| Separate Workflow + Signals | High | Yes | Yes | High | Yes |
| Async Lambda | Low | No | No | Very Low | No |
| Async Lambda | Low | No | No | Very Low |

## Related Patterns

- **Parallel Execution**: Running multiple children concurrently
- **Continue-As-New**: Child workflows can use continue-as-new independently
- **Saga Pattern**: Children as compensatable transactions
- **Batch Processing**: Parent coordinates multiple child workers
- **Fire-and-Forget**: Async children with ABANDON policy

## Sample Code

- [HelloChild](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/hello/HelloChild.java) - Basic synchronous child workflow
- [Async Child Workflow](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/asyncchild) - Asynchronous child with ABANDON policy
- [Async Untyped Child](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/asyncuntypedchild) - Untyped async child workflow

## Best Practices

1. **Use Unique Workflow IDs**: Generate unique IDs for child workflows to avoid conflicts
2. **Choose Appropriate Policy**: Use TERMINATE for tightly coupled, ABANDON for independent children
3. **Handle Child Failures**: Catch and handle child workflow exceptions appropriately
4. **Limit Parallelism**: Don't spawn unlimited children; use batch patterns for large datasets
5. **Consider Activities First**: Use activities for simple operations; reserve children for complex logic
6. **Set Timeouts**: Configure appropriate workflow execution timeouts for children
7. **Use Typed Stubs**: Prefer typed stubs over untyped for compile-time safety
8. **Monitor Child Executions**: Track child workflow IDs for observability and debugging
