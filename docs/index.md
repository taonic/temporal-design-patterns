# Temporal Design Patterns - Common Catalog

> **Warning:** This catalog is under active development. Content and structure may change.
>
> **Personal project by [@taonic](https://github.com/taonic).**

Temporal provides a set of durable execution primitives that you can compose into common, reusable, and proven patterns.
Having these patterns in your toolbox helps you solve recurring problems in a battle-tested way.

## Distributed transaction patterns

### [Saga Pattern](saga-pattern.md)

Manages distributed transactions with compensating actions.
Each step has a compensation that undoes its effects if subsequent steps fail.

### [Early Return, a.k.a Update with Start](early-return.md)

Synchronous initialization with asynchronous completion.
Returns results immediately while processing continues in the background.

## Stateful / lifecycle patterns

### [Entity Workflow](entity-workflow.md)

Models long-lived business entities (users, accounts, devices) as individual Workflows that persist for the entity's entire lifetime.
Each entity gets its own Workflow instance handling all state transitions through Signals and Updates.

### [Continue-As-New](continue-as-new.md)

Prevents unbounded history growth by starting a new execution with fresh history.

### [Child Workflows](child-workflows.md)

Decomposes complex Workflows into smaller, reusable Workflow units.
Each child has an independent Workflow ID, history, and lifecycle with flexible parent-child coordination.

### Query for state inspection

Read-only operations that expose Workflow state without modification.

### Workflow Updates

Synchronous state modification with validation and direct result return.

### Memo and Search Attributes

Attaches metadata for filtering and discovery.
Memos store data; Search Attributes enable querying.

## Event-driven patterns

### [Signal with Start](signal-with-start.md)

Starts a Workflow when Signaling it if it does not already exist.
If the Workflow is already running, it receives the Signal; if not, it starts first and then receives the Signal.
This pattern fits entity Workflows that should only exist when needed.

### [Request-Response via Updates](request-response-via-updates.md)

Synchronous request-response with validation.
Updates modify state and return results directly.

### [Updatable Timer](updatable-timer.md)

Dynamically adjustable timers that respond to Signals or Updates.
You can extend, shorten, or cancel timers based on external events.

### Nexus cross-Namespace operations

Invokes operations across Namespace boundaries with cancellation and context propagation.

## Business process patterns

### [Approval](approval.md)

Human-in-the-loop Workflows that block until external approval decisions are made.
Uses Signals to capture approval data with metadata.

### [Delayed Start](delayed-start.md)

Creates Workflows immediately but defers execution until a specified delay expires.
This pattern fits one-time scheduled operations and grace periods.

### Scheduled Workflows

Executes Workflows on recurring Schedules.

## Long-running and operational patterns

### [Polling External Services](polling.md)

Strategies for polling external resources with varying frequencies.

### Retry policies

Automatic retry with exponential backoff and non-retryable error types.

### [Long-running Activity - tracking progress and handling cancellation with heartbeats](long-running-activity.md)

Long-running Activities report progress and enable resumption after failures.

### Cancellation handling

Graceful Workflow and Activity cancellation with cleanup.

### [Parallel Execution](parallel-execution.md)

Executes multiple Activities concurrently for maximum throughput.

### [Pick First (Race)](pick-first.md)

Starts multiple Activities in parallel and uses the first result.

### Batch processing

Processes large datasets efficiently with various strategies.

### [Worker-Specific Task Queues](worker-specific-taskqueue.md)

Routes Activities to specific Workers using unique Task Queues for Worker affinity.

### Worker versioning

Manages Workflow code changes safely using build IDs and version sets.

## Cross-cutting patterns

### Context propagation

Propagates tracing context and metadata across Workflow boundaries.

### Encryption

Encrypts Workflow and Activity payloads using custom data converters.

### Interceptors

Implements cross-cutting concerns like logging, metrics, and custom retry logic.
