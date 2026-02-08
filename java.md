# Temporal Design Patterns

A comprehensive collection of design patterns found in the Temporal Java SDK samples, organized by category.

---

## 1. Distributed Transaction Patterns

### SAGA Pattern
**Location**: `bookingsaga/`, `bookingsyncsaga/`, `hello/HelloSaga.java`

Implements distributed transactions with compensating actions. When a workflow executes multiple activities that modify external state, the SAGA pattern ensures that if any step fails, all previously completed steps are compensated (undone) in reverse order. Temporal's built-in `Saga` class supports both sequential and parallel compensation execution.

### Two-Phase Commit (Money Transfer)
**Location**: `moneytransfer/`, `earlyreturn/`

Demonstrates atomic operations across distributed systems by executing withdraw and deposit activities sequentially. The workflow ensures that funds are withdrawn before depositing, maintaining consistency. The early return pattern allows returning transaction status to clients before the full workflow completes.

### Batch Aggregation (Money Batch)
**Location**: `moneybatch/`

Collects multiple withdrawal requests and executes a single deposit operation when a threshold is reached. Uses `Workflow.await()` to block until the batch size condition is met, demonstrating how to aggregate distributed operations for efficiency.

### Idempotent Operations
**Location**: `moneybatch/`, `safemessagepassing/`

Ensures operations can be safely retried by tracking processed reference IDs in workflow state. Duplicate signals or updates are detected and ignored, preventing double-processing in distributed scenarios where messages may be delivered multiple times.

---

## 2. Event-Driven and Task-Queue Patterns

### Signal-Based Event Handling
**Location**: `hello/HelloSignal.java`, `hello/HelloSignalWithTimer.java`

Workflows receive external events via signals, storing them in an internal queue and processing them asynchronously. The workflow blocks using `Workflow.await()` until signals arrive or an exit condition is met, enabling reactive event-driven architectures.

### Signal with Start
**Location**: `hello/HelloSignalWithStartAndWorkflowInit.java`, `moneybatch/`

Lazily starts a workflow when signaling it. If the workflow is already running, it receives the signal; if not, it starts first and then receives the signal. This pattern is ideal for entity workflows that should only exist when needed.

### Update with Start (Early Return)
**Location**: `earlyreturn/`

Combines workflow start with synchronous updates, allowing clients to receive early results before the workflow completes. The update handler waits for initialization to complete and returns intermediate results, while the main workflow continues processing.

### Host-Specific Task Queues
**Location**: `fileprocessing/`

Routes activities to specific workers based on affinity requirements. The first activity returns a host-specific task queue name, and subsequent activities use that queue to ensure they execute on the same host where temporary files were created.

### Dynamic Activity Routing
**Location**: `dsl/`

Executes workflows defined by JSON/DSL specifications, dynamically creating activity stubs and routing to different activity types based on runtime configuration. Enables workflow-as-configuration patterns.

---

## 3. Stateful / Lifecycle Patterns

### Entity Workflow (Cluster Manager)
**Location**: `safemessagepassing/`

Long-running workflow representing a stateful entity (cluster) that responds to signals and updates to manage its lifecycle. Uses `WorkflowLock` to safely handle concurrent state modifications from multiple signals/updates, and periodically continues-as-new to prevent unbounded history growth.

### Query for State Inspection
**Location**: `hello/HelloQuery.java`

Exposes workflow internal state to external clients via query methods without modifying state. Queries are synchronous, read-only operations that return current workflow state, enabling observability and monitoring.

### Update for State Mutation
**Location**: `hello/HelloUpdate.java`

Allows external clients to synchronously modify workflow state and receive confirmation. Updates can validate inputs, mutate state, invoke activities, and return results. Unlike signals, updates are tracked in history and can fail with typed errors.

### Updatable Timer
**Location**: `updatabletimer/`

Implements a sleep operation that can be interrupted and updated dynamically via signals. Uses `Workflow.await()` with a time condition that can be modified, allowing workflows to adjust their timing based on external events.

### Continue-As-New for Long-Running Workflows
**Location**: `hello/HelloPeriodic.java`, `batch/slidingwindow/`, `safemessagepassing/`

Prevents unbounded history growth by periodically checkpointing state and continuing execution as a new workflow run. Essential for workflows that run indefinitely or process large numbers of iterations.

### Workflow Init Pattern
**Location**: `safemessagepassing/`, `hello/HelloSignalWithStartAndWorkflowInit.java`

Uses `@WorkflowInit` constructor to initialize workflow state before the main method executes. Particularly useful with signal-with-start to ensure proper initialization when signals arrive before the workflow method starts.

---

## 4. Business Process & Human-in-the-Loop Patterns

### Approval Workflow (Updatable Timer)
**Location**: `updatabletimer/`

Implements time-based approval processes where deadlines can be extended. The workflow sleeps until a deadline, but signals can update the wake-up time, modeling scenarios like approval requests with deadline extensions.

### Accumulator Pattern
**Location**: `hello/HelloAccumulator.java`

Collects signals over time, accumulating state, then continues-as-new to process the accumulated data. Useful for gathering inputs from multiple sources before proceeding with business logic.

### Exclusive Choice (Conditional Routing)
**Location**: `hello/HelloActivityExclusiveChoice.java`

Executes different activities based on dynamic input conditions, implementing business rule routing. The workflow evaluates conditions and selects appropriate execution paths at runtime.

### Scheduled Workflows
**Location**: `hello/HelloSchedules.java`, `hello/HelloCron.java`

Executes workflows on recurring schedules using Temporal's Schedule API or cron expressions. Ideal for periodic business processes like reports, reconciliation, or maintenance tasks.

### Delayed Start
**Location**: `hello/HelloDelayedStart.java`

Starts workflow execution at a future time using workflow options. Useful for scheduling business processes to begin at specific times without external schedulers.

---

## 5. Long-Running and Operational Patterns

### Polling External Services
**Location**: `polling/infrequent/`, `polling/frequent/`, `polling/periodicsequence/`

Implements various strategies for polling external services:
- **Infrequent polling**: Uses activity retry with fixed backoff intervals
- **Frequent polling**: Uses workflow timers with short intervals
- **Periodic sequence**: Uses child workflows for each poll attempt

### Batch Processing Patterns
**Location**: `batch/heartbeatingactivity/`, `batch/iterator/`, `batch/slidingwindow/`

Three approaches to processing large datasets:
- **Heartbeating Activity**: Single long-running activity with heartbeats and checkpointing
- **Iterator**: Parent workflow spawns child workflows for each record
- **Sliding Window**: Maintains fixed number of concurrent child workflows, continues-as-new periodically

### Async Activity Completion
**Location**: `hello/HelloAsyncActivityCompletion.java`

Activities complete asynchronously via external systems. The activity returns a completion token, and an external process completes the activity later, enabling human tasks or long-running external processes.

### Async Child Workflows
**Location**: `asyncchild/`, `asyncuntypedchild/`

Parent workflow starts child workflows asynchronously and doesn't wait for completion. Children can outlive the parent by using `PARENT_CLOSE_POLICY_ABANDON`, enabling fire-and-forget patterns.

### Parallel Execution
**Location**: `hello/HelloParallelActivity.java`, `hello/HelloAsync.java`

Executes multiple activities concurrently using `Async.function()` and `Promise.allOf()`. Maximizes throughput by parallelizing independent operations.

### Cancellation Scopes
**Location**: `hello/HelloCancellationScope.java`, `hello/HelloDetachedCancellationScope.java`

Controls cancellation propagation within workflows. Detached scopes allow cleanup activities to run even when the workflow is cancelled, ensuring proper resource cleanup.

### Workflow Timers vs Execution Timeouts
**Location**: `hello/HelloWorkflowTimer.java`, `hello/HelloCancellationScopeWithTimer.java`

Uses explicit workflow timers instead of execution timeouts to control workflow duration. Provides more control over timeout behavior and allows graceful cleanup when time limits are reached.

### Retry Strategies
**Location**: `hello/HelloActivityRetry.java`, `peractivityoptions/`

Configures activity-specific retry policies with backoff, maximum attempts, and non-retryable error types. Demonstrates how to handle transient failures while failing fast on permanent errors.

### Auto-Heartbeating
**Location**: `autoheartbeat/`

Implements automatic activity heartbeating via interceptors, removing the need for manual heartbeat calls in activity code. Ensures long-running activities report progress without code changes.

### Worker Versioning
**Location**: `workerversioning/`

Manages workflow code changes over time using worker versioning. Allows deploying new workflow versions while continuing to execute existing workflows with old code, enabling safe deployments.

### Safe Message Passing with Locks
**Location**: `safemessagepassing/`

Uses `WorkflowLock` to synchronize access to shared state when handling concurrent signals and updates. Prevents race conditions in entity workflows that receive multiple concurrent messages.

### Side Effects for Non-Deterministic Operations
**Location**: `hello/HelloSideEffect.java`

Wraps non-deterministic operations (like random number generation or UUID creation) in `Workflow.sideEffect()` to ensure deterministic replay. The result is recorded in history and reused on replay.

### Search Attributes for Workflow Discovery
**Location**: `hello/HelloSearchAttributes.java`, `listworkflows/`

Adds custom search attributes to workflows for filtering and discovery. Enables querying workflows by business attributes like customer ID, order status, or region.

### Packet Delivery (Async Parallel Paths)
**Location**: `packetdelivery/`

Executes multiple independent execution paths asynchronously within a single workflow. Each path processes data independently, and the workflow completes when all paths finish.

---

## Cross-Cutting Patterns

### Interceptors
**Location**: `countinterceptor/`, `retryonsignalinterceptor/`, `excludefrominterceptor/`, `autoheartbeat/`

Implements cross-cutting concerns like metrics, logging, custom retry logic, and auto-heartbeating by intercepting workflow and activity invocations.

### Custom Payload Converters
**Location**: `payloadconverter/cloudevents/`, `payloadconverter/crypto/`

Customizes serialization/deserialization of workflow inputs and outputs. Enables integration with external formats (CloudEvents) or encryption of sensitive data.

### Payload Codecs for Encryption
**Location**: `encryptedpayloads/`, `keymanagementencryption/awsencryptionsdk/`, `encodefailures/`

Encrypts/decrypts workflow data at rest and in transit using payload codecs. Ensures sensitive data is never stored in plaintext in Temporal's history.

### Nexus Service Integration
**Location**: `nexus/`, `nexuscancellation/`, `nexuscontextpropagation/`, `nexusmultipleargs/`

Integrates with external services via Temporal Nexus, enabling cross-namespace and cross-cluster workflow orchestration with proper context propagation and cancellation handling.

---

## Summary

This codebase demonstrates **50+ distinct patterns** across five major categories:

1. **Distributed Transactions** (4 patterns): SAGA, two-phase commit, batch aggregation, idempotency
2. **Event-Driven** (5 patterns): Signals, signal-with-start, update-with-start, task queue routing, dynamic routing
3. **Stateful/Lifecycle** (6 patterns): Entity workflows, queries, updates, updatable timers, continue-as-new, workflow init
4. **Business Process** (6 patterns): Approvals, accumulators, conditional routing, schedules, delayed start
5. **Long-Running/Operational** (20+ patterns): Polling, batch processing, async completion, parallel execution, cancellation, retries, versioning, etc.

These patterns provide a comprehensive toolkit for building reliable, scalable, and maintainable distributed applications with Temporal.
