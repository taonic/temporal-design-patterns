# Temporal Design Patterns

A comprehensive collection of design patterns found in the Temporal Java SDK samples, organized by category.


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

