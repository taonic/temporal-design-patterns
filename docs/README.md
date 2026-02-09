# Temporal Design Patterns - Common Catalog

> **⚠️ Work In Progress**: This catalog is currently under active development. Content and structure may change.
>
> **Personal project by [@taonic](https://github.com/taonic).**

Temporal has a set of durable execution primitives that can be composed into common, reusable, and proven patterns. Having these patterns in your toolbox helps you solve recurring problems in a battle-tested way.

## Distributed Transaction Patterns

### [Saga Pattern](saga-pattern.md)

Manages distributed transactions with compensating actions. Each step has a compensation that undoes its effects if subsequent steps fail.

### [Early Return, a.k.a Update with Start](early-return.md)

Synchronous initialization with asynchronous completion. Returns results immediately while processing continues in background.


## Stateful / Lifecycle Patterns

### [Continue-As-New](continue-as-new.md)

Prevents unbounded history growth by starting new execution with fresh history.

### [Child Workflows](child-workflows.md)

Decomposes complex workflows into smaller, reusable workflow units. Each child has independent workflow ID, history, and lifecycle with flexible parent-child coordination.

### Query for State Inspection

Read-only operations that expose workflow state without modification.

### Workflow Updates

Synchronous state modification with validation and direct result return.

### Memo and Search Attributes

Attaches metadata for filtering and discovery. Memos store data; search attributes enable querying.


## Long-Running and Operational Patterns

### [Polling External Services](polling.md)

Strategies for polling external resources with varying frequencies.

### Retry Policies

Automatic retry with exponential backoff and non-retryable error types.

### [Long running Activity - tracking progress and handle cancellation with heartbeats](long-running-activity.md)

Long-running activities report progress and enable resumption after failures.

### Cancellation Handling

Graceful workflow and activity cancellation with cleanup.

### [Parallel Execution](parallel-execution.md)

Executes multiple activities concurrently for maximum throughput.

### [Pick First (Race)](pick-first.md)

Starts multiple activities in parallel and uses first result.

### Batch Processing

Processes large datasets efficiently with various strategies.

### [Worker-Specific Task Queues](worker-specific-taskqueue.md)

Routes activities to specific workers using unique task queues for worker affinity.

### Worker Versioning

Manages workflow code changes safely using build IDs and version sets.

