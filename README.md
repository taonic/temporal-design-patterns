# Temporal Design Patterns - Common Catalog

Temporal has a set of durable execution primitives that can be composed into common, reusable, and proven patterns. Having these patterns in your toolbox helps you solve recurring problems in a battle-tested way.

## Distributed Transaction Patterns

### [Saga Pattern](saga-pattern.md)

Manages distributed transactions with compensating actions. Each step has a compensation that undoes its effects if subsequent steps fail.

### [Early Return, a.k.a Update with Start](early-return.md)

Synchronous initialization with asynchronous completion. Returns results immediately while processing continues in background.

---

## Event-Driven Patterns

### [Signal with Start](signal-with-start.md)

Lazily starts a workflow when signaling it. If the workflow is already running, it receives the signal; if not, it starts first and then receives the signal. This pattern is ideal for entity workflows that should only exist when needed.

### [Request-Response via Updates](request-response-via-updates.md)

Synchronous request-response with validation. Updates modify state and return results directly.

### Worker-Specific Task Queues

Routes activities to specific workers using unique task queues for worker affinity.

### Nexus Cross-Namespace Operations

Invokes operations across namespace boundaries with cancellation and context propagation.

---

## Stateful / Lifecycle Patterns

### Continue-As-New

Prevents unbounded history growth by starting new execution with fresh history.

### Child Workflows

Decomposes complex workflows into manageable sub-workflows.

### Query for State Inspection

Read-only operations that expose workflow state without modification.

### Workflow Updates

Synchronous state modification with validation and direct result return.

### Memo and Search Attributes

Attaches metadata for filtering and discovery. Memos store data; search attributes enable querying.

---

## Business Process Patterns

### Async Activity Completion

Activities complete outside worker process via external systems or human approval.

### Scheduled Workflows

Executes workflows on recurring schedules.

### Cron Workflows

Recurring workflows using cron expressions.

### Exclusive Choice (Conditional Routing)

Routes execution based on dynamic input conditions.

---

## Long-Running and Operational Patterns

### Timers

Time-based workflow logic with delays and deadlines.

### Polling External Services

Strategies for polling external resources with varying frequencies.

### Retry Policies

Automatic retry with exponential backoff and non-retryable error types.

### Heartbeats and Progress Tracking

Long-running activities report progress and enable resumption after failures.

### Cancellation Handling

Graceful workflow and activity cancellation with cleanup.

### Parallel Execution

Executes multiple activities concurrently for maximum throughput.

### Pick First (Race)

Starts multiple activities in parallel and uses first result.

### Batch Processing

Processes large datasets efficiently with various strategies.

### Worker Versioning

Manages workflow code changes safely using build IDs and version sets.

---

## Cross-Cutting Patterns

### Context Propagation

Propagates tracing context and metadata across workflow boundaries.

### Encryption

Encrypts workflow and activity payloads using custom data converters.

### Interceptors

Implements cross-cutting concerns like logging, metrics, and custom retry logic.
