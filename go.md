# Temporal Design Patterns

This document catalogs the design patterns demonstrated in the Temporal Go SDK samples, organized by category.

## Distributed Transaction Patterns

### Saga Pattern
**Location:** `saga/`

#### Intent
Manage distributed transactions across multiple services by coordinating a sequence of local transactions, each with a compensating action that can undo its effects if subsequent steps fail.

#### Problem
In distributed systems, you need to maintain data consistency across multiple services or databases without using traditional ACID transactions. When a multi-step business process fails partway through, you must undo the effects of completed steps to maintain system consistency. Traditional two-phase commit doesn't scale well and creates tight coupling between services.

#### Solution
Implement each step as a local transaction with a corresponding compensation transaction. If any step fails, execute compensation transactions in reverse order to undo the effects of all completed steps. Use Go's `defer` mechanism to automatically trigger compensations when errors occur, ensuring cleanup happens even if the workflow logic panics or returns early.

#### Structure

**Go Implementation** (using `defer`):
```go
func TransferMoney(ctx workflow.Context, details TransferDetails) error {
    // Step 1: Withdraw from source account
    err := workflow.ExecuteActivity(ctx, Withdraw, details).Get(ctx, nil)
    if err != nil {
        return err
    }
    
    // Register compensation for Step 1
    defer func() {
        if err != nil {
            _ = workflow.ExecuteActivity(ctx, WithdrawCompensation, details).Get(ctx, nil)
        }
    }()
    
    // Step 2: Deposit to target account
    err = workflow.ExecuteActivity(ctx, Deposit, details).Get(ctx, nil)
    if err != nil {
        return err // Triggers defer, which runs WithdrawCompensation
    }
    
    // Register compensation for Step 2
    defer func() {
        if err != nil {
            _ = workflow.ExecuteActivity(ctx, DepositCompensation, details).Get(ctx, nil)
        }
    }()
    
    // Step 3: Additional operation
    err = workflow.ExecuteActivity(ctx, StepWithError, details).Get(ctx, nil)
    return err // If error, both compensations run in reverse order
}
```

**Java Implementation** (using Saga API):
```java
public class HelloSaga {
    @WorkflowInterface
    public interface GreetingWorkflow {
        @WorkflowMethod
        String getGreeting(String name);
    }

    public static class GreetingWorkflowImpl implements GreetingWorkflow {
        @Override
        public String getGreeting(String name) {
            // Create a Saga instance with compensation options
            Saga saga = new Saga(new Saga.Options.Builder()
                .setParallelCompensation(false) // Run compensations sequentially
                .build());
            
            try {
                // Step 1: Execute activity and register compensation
                String hello = Workflow.executeActivity(
                    activities::hello, 
                    String.class, 
                    name
                ).get();
                saga.addCompensation(activities::cleanupHello, name);
                
                // Step 2: Execute activity and register compensation
                String bye = Workflow.executeActivity(
                    activities::bye, 
                    String.class, 
                    name
                ).get();
                saga.addCompensation(activities::cleanupBye, name);
                
                // Step 3: This might fail
                Workflow.executeActivity(
                    activities::processFile, 
                    Void.class, 
                    name
                ).get();
                saga.addCompensation(activities::cleanupFile, name);
                
                return hello + "; " + bye;
                
            } catch (Exception e) {
                // On any error, run all registered compensations in reverse order
                saga.compensate();
                throw e;
            }
        }
    }
}
```

**Key Differences:**
- **Go**: Uses `defer` statements that execute in LIFO order when function returns
- **Java**: Uses explicit `Saga` object to track and trigger compensations
- **Both**: Compensations run in reverse order of registration
- **Both**: Compensations are idempotent and can handle partial failures

#### Applicability
Use the Saga pattern when:
- You need to maintain consistency across multiple services or databases
- Traditional distributed transactions (2PC) are too slow or unavailable
- You can define compensating actions for each step in your business process
- Eventual consistency is acceptable for your use case
- You need to handle long-running transactions that may span hours or days

#### Pros
- ✅ Maintains eventual consistency without distributed locks
- ✅ Each service can use its own database and transaction model
- ✅ Automatic compensation execution via `defer` ensures cleanup
- ✅ Scales better than two-phase commit protocols
- ✅ Temporal's durability guarantees compensations will execute even after worker failures

#### Cons
- ❌ Eventual consistency only - intermediate states are visible to other processes
- ❌ Requires careful design of idempotent compensation activities
- ❌ More complex than simple ACID transactions
- ❌ Compensation logic must be maintained alongside forward logic
- ❌ Some operations may not have meaningful compensations

#### Relations with Other Patterns
- Often combined with **Retry Policies** to handle transient failures before compensating
- Can use **Child Workflows** to organize complex sagas with multiple sub-sagas
- May leverage **Async Activity Completion** when compensations require external approval
- Works well with **Heartbeats** for long-running compensation activities

### Mutex/Distributed Lock
**Location:** `mutex/`

#### Intent
Provide exclusive access to shared resources across distributed workflow executions.

#### Problem
Multiple workflow executions may need to access the same resource (database record, external API, file) but only one should access it at a time to prevent race conditions or conflicting updates.

#### Solution
Uses signal-based coordination where a dedicated mutex workflow manages lock acquisition and release. Workflows request locks via signals, receive unique release channels, and can timeout if locks aren't released. Prevents race conditions and ensures mutually exclusive operations on the same resource across multiple workflow instances.

### Two-Phase Operations (Early Return)
**Location:** `early-return/`

Demonstrates synchronous initialization with asynchronous completion. Uses Update-with-Start to return transaction initialization results immediately while processing continues asynchronously. The workflow validates and initializes a transaction quickly (using local activities), returns the result to the caller, then completes or cancels the transaction in the background based on initialization success.

## Event-Driven and Task-Queue Patterns

### Signal-Based Communication
**Location:** `recovery/`, `mutex/`, `synchronous-proxy/`

Enables external events to influence running workflows. Workflows register signal handlers and wait for external signals to trigger state transitions. Used for human-in-the-loop scenarios, inter-workflow communication, and responding to external system events without polling.

### Request-Response via Signals
**Location:** `synchronous-proxy/`

Implements synchronous request-response patterns using signals. A proxy workflow sends a signal to a main workflow and blocks waiting for a response signal. Enables interactive workflows where external systems can query and receive responses from long-running workflow state.

### Request-Response via Updates
**Location:** `reqrespupdate/`

Uses workflow updates for synchronous request-response with validation. Updates provide stronger guarantees than signals - they're validated before acceptance, return responses directly, and are tracked in workflow history. Ideal for operations that modify workflow state and need immediate feedback.

### Request-Response via Queries
**Location:** `reqrespquery/`

Implements polling-based request-response using queries. Requests are sent via signals and stored in workflow state, while clients poll using queries to retrieve responses. Queries are read-only and don't modify workflow state, making them suitable for status checks and data retrieval.

### Request-Response via Activities
**Location:** `reqrespactivity/`

Uses callback activities to push responses back to requesters. Workflows receive requests via signals, process them through activities, then invoke response activities on the requester's task queue. Enables asynchronous request-response where the requester doesn't need to poll, but must have a worker running to receive responses.

### Worker-Specific Task Queues
**Location:** `worker-specific-task-queues/`

Routes activities to specific workers using unique task queues. Each worker registers with a unique task queue identifier, and workflows route activities requiring worker affinity (e.g., local file access) to that specific queue. Ensures activities that depend on worker-local state execute on the correct host.

### Nexus Cross-Namespace Operations
**Location:** `nexus/`, `nexus-cancelation/`, `nexus-context-propagation/`, `nexus-multiple-arguments/`

Enables workflows to invoke operations across namespace boundaries. Nexus provides a service-oriented abstraction for cross-namespace calls with support for cancellation propagation, context passing, and multiple argument handling. Useful for building multi-tenant systems or separating concerns across different Temporal namespaces.

## Stateful / Lifecycle Patterns

### Continue-As-New
**Location:** `child-workflow-continue-as-new/`, `reqrespupdate/`, `cron/`

Prevents unbounded workflow history growth by starting a new execution with fresh history. The workflow completes with a special error that instructs Temporal to immediately start a new run with specified parameters. Essential for long-running workflows that process many events or iterations, as it keeps history size manageable while maintaining logical continuity.

### Child Workflows
**Location:** `child-workflow/`, `child-workflow-continue-as-new/`

Decomposes complex workflows into manageable sub-workflows. Parent workflows spawn child workflows that execute independently but report results back to the parent. Child workflows can continue-as-new without affecting the parent, enabling modular workflow design and separation of concerns.

### Session Affinity
**Location:** `fileprocessing/`, `session-failure/`

Binds a sequence of activities to the same worker. Creates a session that reserves a worker for multiple related activities, ensuring they execute on the same host. Critical for workflows where activities share local state (downloaded files, cached data, database connections) that shouldn't be replicated across workers.

### Workflow State Management
**Location:** `safe_message_handler/`

Demonstrates safe concurrent handling of signals and updates. Uses proper synchronization to prevent race conditions when multiple signals/updates arrive simultaneously. Ensures workflow state remains consistent even under concurrent message delivery.

### Query for State Inspection
**Location:** `query/`, `pso/`

Exposes workflow internal state without modifying it. Queries are read-only operations that return current workflow state to external callers. Unlike signals or updates, queries don't appear in workflow history and don't affect execution, making them ideal for monitoring and debugging. The PSO example demonstrates querying child workflow IDs from parent workflows.

### Workflow Updates
**Location:** `update/`, `shoppingcart/`

Enables synchronous modification of workflow state with validation. Updates are validated before acceptance, execute within the workflow context, and return results directly to callers. The shopping cart example shows a long-running workflow that processes add/remove/list operations via updates, with validators ensuring data integrity.

### Memo and Search Attributes
**Location:** `memo/`, `searchattributes/`, `typed-searchattributes/`

Attaches metadata to workflows for filtering and discovery. Memos store arbitrary data with workflows (not indexed), while search attributes are indexed fields that enable querying workflows by custom criteria. Search attributes can be upserted during workflow execution and used to find workflows via list/query APIs.

## Business Process & Human-in-the-Loop Patterns

### Async Activity Completion
**Location:** `expense/`

Handles activities that complete outside the worker process. The activity returns a task token and completes asynchronously when an external system (human approval, webhook callback) provides the result. Enables workflows to wait for human decisions, external API callbacks, or long-running external processes without blocking workers.

### Interactive Workflows (Synchronous Proxy)
**Location:** `synchronous-proxy/`

Builds multi-step interactive processes with validation. The workflow loops through stages, validating user input at each step via activities. Invalid input is rejected with error responses, allowing users to retry. Demonstrates building wizard-like flows where each step depends on validated previous inputs.

### Await Signal Processing
**Location:** `await-signals/`

Handles out-of-order signal delivery gracefully. Uses `Await` and `AwaitWithTimeout` to wait for specific conditions before processing signals. Ensures signals are processed in the correct logical order even if they arrive out of sequence, maintaining workflow state consistency.

### Scheduled Workflows
**Location:** `schedule/`

Executes workflows on a recurring schedule. Temporal Schedules provide cron-like functionality with better observability and control. Each scheduled run is a separate workflow execution, allowing independent monitoring and management of each occurrence.

### Cron Workflows (Legacy)
**Location:** `cron/`

Implements recurring workflows using cron expressions. Each execution can access results from the previous run via `GetLastCompletionResult`, enabling stateful recurring processes. Note: Temporal Schedules are now recommended over cron workflows for new implementations.

### Conditional Execution Patterns
**Location:** `choice-exclusive/`, `choice-multi/`

Routes workflow execution based on dynamic input:
- **Exclusive Choice:** Executes one activity selected by a switch statement based on runtime data
- **Multi-Choice:** Executes multiple activities in parallel based on a list of choices

Enables data-driven workflow logic where execution paths are determined by activity results or input parameters.

## Long-Running and Operational Patterns

### Timers and Deadlines
**Location:** `timer/`, `updatabletimer/`

Implements time-based workflow logic. Workflows can set timers for delays or deadlines, and cancel them if conditions change. The updatable timer pattern shows how to extend or cancel timers based on signals, useful for SLA monitoring or timeout management.

### Polling External Services
**Location:** `polling/infrequent/`, `polling/frequent/`, `polling/periodic_sequence/`

Demonstrates different strategies for polling external resources:
- **Infrequent:** Uses activity retry with long intervals (backoff coefficient of 1) to poll every N seconds
- **Frequent:** Polls in tight loops with short sleeps for near-real-time monitoring
- **Periodic Sequence:** Uses child workflows with continue-as-new for long-running periodic checks

### Retry Policies
**Location:** `retryactivity/`

Configures automatic retry behavior for transient failures. Activities can specify retry policies with exponential backoff, maximum attempts, and non-retryable error types. Combined with heartbeats, activities can resume from their last reported progress after failures.

### Heartbeats and Progress Tracking
**Location:** `retryactivity/`, `fileprocessing/`, `recovery/`

Enables long-running activities to report progress and detect failures. Activities periodically send heartbeats with progress information. If a worker crashes, the activity can be retried on another worker and resume from the last heartbeat. Also allows workflows to detect stuck activities via heartbeat timeouts.tivity can be retried on another worker and resume from the last heartbeat. Also allows workflows to detect stuck activities via heartbeat timeouts.

### Cancellation Handling
**Location:** `cancellation/`

Gracefully handles workflow and activity cancellation. Workflows can defer cleanup activities that execute even when cancelled, ensuring resources are properly released. Activities check cancellation context and can perform cleanup before terminating.

### Parallel Execution Patterns

#### Fan-Out/Fan-In (Split-Merge)
**Location:** `splitmerge-future/`, `splitmerge-selector/`

Executes multiple activities in parallel and aggregates results:
- **Future-based:** Waits for results in invocation order using `Future.Get()`
- **Selector-based:** Processes results as they complete using `Selector`, enabling early processing of fast activities

#### Pick First (Race)
**Location:** `pickfirst/`

Starts multiple activities in parallel and uses the first result. Remaining activities are cancelled once the first completes. Useful for redundant operations, fastest-source selection, or timeout alternatives.

#### Parallel Branches
**Location:** `branch/`, `goroutine/`

Executes multiple workflow branches concurrently using `workflow.Go()`. Each branch runs in a deterministic coroutine, allowing parallel logic while maintaining workflow determinism. The number of branches can be dynamic based on input parameters.

### Selectors for Non-Deterministic Choice
**Location:** `pickfirst/`, `splitmerge-selector/`, `mutex/`, `timer/`, `updatabletimer/`

Uses `workflow.Selector` to wait on multiple channels/futures simultaneously. Selectors enable workflows to react to whichever event occurs first (signal, timer, activity completion) without blocking on a specific one. Essential for implementing timeouts, cancellation, and event-driven logic while maintaining determinism.

### Dynamic Workflow Execution
**Location:** `dynamic/`, `dynamic-workflows/`, `dsl/`

Executes workflows and activities by name rather than strongly-typed functions. Enables:
- **Dynamic dispatch:** Route to different implementations based on runtime parameters
- **DSL-based workflows:** Define workflow logic in YAML/JSON and execute via a generic workflow interpreter (DSL example uses YAML to define workflow steps)
- **Plugin architectures:** Load and execute workflow logic without recompiling

### Complex Iterative Workflows (PSO)
**Location:** `pso/`

Demonstrates particle swarm optimization - a complex, long-running iterative computation. Shows how to:
- Use child workflows with continue-as-new for unbounded iterations
- Implement custom data converters for complex types
- Query workflow state during execution
- Retry entire optimization runs with different parameters

Useful pattern for any long-running iterative algorithm (machine learning, simulations, optimization).

### Workflow Recovery and Migration
**Location:** `recovery/`

Rebuilds failed workflows by extracting state from history. Lists open workflows, retrieves their history, extracts initialization parameters and signals, terminates the old execution, and starts a new one with replayed signals. Useful for recovering from bugs or migrating workflows to new versions.

### Worker Versioning
**Location:** `worker-versioning/`

Manages workflow code changes safely. Uses build IDs and version sets to route workflow tasks to compatible workers. Enables gradual rollout of workflow changes without breaking in-flight executions.

### Batch Processing
**Location:** `batch-sliding-window/`

Processes large datasets efficiently using sliding windows. Workflows coordinate batch processing across multiple workers, managing throughput and resource utilization. Demonstrates patterns for high-volume data processing with Temporal.

### Long-Running Workflows
**Location:** `sleep-for-days/`

Demonstrates workflows that sleep for extended periods (days, weeks, months). Temporal efficiently handles long timers without consuming resources during the wait period. Useful for scheduled reminders, delayed notifications, or time-based business processes.

### Workflow Start Delay
**Location:** `start-delay/`

Schedules workflow execution to start at a future time. The workflow is created immediately but doesn't begin executing until the specified delay elapses. Useful for scheduling future work without using external schedulers.

### Eager Workflow Start
**Location:** `eager-workflow-start/`

Optimization that starts workflow execution on the same worker that received the start request, avoiding a round-trip to the server. Reduces latency for short-lived workflows by executing the first workflow task immediately if a worker is available on the client connection.

### Observability Patterns

#### Context Propagation
**Location:** `ctxpropagation/`, `nexus-context-propagation/`

Propagates tracing context, user identity, and metadata across workflow and activity boundaries. Custom context propagators extract values from client context and inject them into workflow/activity contexts, enabling distributed tracing and audit logging.

#### OpenTelemetry Integration
**Location:** `opentelemetry/`

Instruments workflows and activities with OpenTelemetry for distributed tracing. Traces span workflow executions, activity executions, and child workflows, providing end-to-end visibility into workflow execution paths and performance.

#### Prometheus Metrics
**Location:** `metrics/`

Exposes Temporal metrics to Prometheus using Uber's Tally library. Enables monitoring of workflow execution rates, activity durations, task queue depths, and worker health.

#### Logging Interceptors and Adapters
**Location:** `logger-interceptor/`, `zapadapter/`, `slogadapter/`

Adds contextual information to logs using interceptors. Interceptors wrap workflow and activity invocations, enriching log entries with workflow IDs, run IDs, activity types, and custom metadata. The adapter examples show integration with popular Go logging libraries (Zap, slog).

#### Datadog Integration
**Location:** `datadog/`

Integrates Temporal metrics with Datadog for monitoring and alerting. Demonstrates configuring the Temporal client to export metrics to Datadog's StatsD endpoint.

### Security Patterns

#### Encryption
**Location:** `encryption/`, `snappycompress/`

Encrypts workflow and activity payloads using custom data converters. Demonstrates payload encryption with compression, ensuring sensitive data is encrypted at rest in Temporal's persistence layer. Includes codec server for decrypting payloads in the UI. The snappycompress example shows compression-only data conversion.

#### Codec Server
**Location:** `codec-server/`, `grpc-proxy/`

Provides remote payload encoding/decoding for Temporal UI and CLI. Codec servers decode encrypted or compressed payloads for display without exposing decryption keys to the UI. The gRPC proxy example shows an alternative implementation using gRPC.

#### Workflow Security Interceptor
**Location:** `workflow-security-interceptor/`

Validates and controls child workflow execution. Interceptors can enforce security policies like allowed workflow types, parameter validation, or access control before child workflows are started.

#### mTLS Authentication
**Location:** `helloworldmtls/`, `dynamicmtls/`

Secures client-server communication with mutual TLS. The dynamic mTLS example shows credential refresh without worker restart, enabling certificate rotation for long-running workers.

#### API Key Authentication
**Location:** `helloworld-apiKey/`

Authenticates with Temporal Cloud using API keys. Simpler than mTLS for development and testing scenarios.

#### JWT Authentication
**Location:** `serverjwtauth/`

Demonstrates JWT-based authentication for self-hosted Temporal Server. Shows how to configure server-side JWT validation and client-side token generation.

### Configuration and Deployment Patterns

#### External Configuration
**Location:** `external-env-conf/`

Externalizes Temporal client configuration to TOML files. Separates connection settings (host, namespace, TLS) from application code, enabling environment-specific configuration without code changes.

#### Activity Dependencies (Greetings)
**Location:** `greetings/`, `greetingslocal/`

Demonstrates passing dependencies to activities defined as struct methods. Activities can access shared resources (database connections, API clients) through struct fields. The local variant shows the same pattern with local activities.

#### Replay Testing
**Location:** `helloworld/`, `multi-history-replay/`

Validates workflow code changes don't break existing executions. Replay tests execute workflow history against current code to detect non-deterministic changes. Multi-history replay tests multiple workflow histories in batch.

### Infrastructure and Fixtures

#### Temporal Fixtures
**Location:** `temporal-fixtures/`

Edge case examples for testing and development:
- **large-event-history:** Workflows with many events for testing history limits
- **largepayload:** Tests handling of large payloads
- **openNclosed:** Workflows in various completion states
- **rainbow-statuses:** Workflows demonstrating all possible status values
- **stuck-workflows:** Simulates stuck/deadlocked workflows

Useful for Temporal internal development, testing UI/CLI tools, and reproducing edge cases.

---

## Pattern Selection Guide

- **Need distributed transactions?** → Saga Pattern
- **Need exclusive resource access?** → Mutex Pattern
- **Need human approval?** → Async Activity Completion
- **Need to poll external APIs?** → Polling Patterns (choose frequency based on requirements)
- **Workflow history growing large?** → Continue-As-New
- **Activities need same worker?** → Session Affinity
- **Need parallel processing?** → Fan-Out/Fan-In or Parallel Branches
- **Need fastest result from multiple sources?** → Pick First
- **Need to expose workflow state?** → Query Pattern
- **Need to modify workflow state externally?** → Update Pattern
- **Long-running activities?** → Heartbeats + Retry Policies
- **Need cross-namespace calls?** → Nexus
- **Need workflow modularity?** → Child Workflows
- **Need immediate response while processing continues?** → Early Return (Update-with-Start)
- **Need to attach metadata for filtering?** → Memo (not indexed) or Search Attributes (indexed)
- **Need conditional execution based on data?** → Exclusive/Multi Choice
- **Need to validate state changes?** → Updates with Validators
- **Need complex iterative computation?** → PSO Pattern (child workflows + continue-as-new)
- **Need to wait on multiple events?** → Selectors
- **Need low-latency workflow start?** → Eager Workflow Start
- **Need to schedule future execution?** → Start Delay or Schedules
- **Need activity dependencies/shared state?** → Greetings Pattern (struct methods)
- **Need to test workflow changes?** → Replay Testing
