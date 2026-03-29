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

## Entity & lifecycle patterns

### [Entity Workflow](entity-workflow.md)

Models long-lived business entities (users, accounts, devices) as individual Workflows that persist for the entity's entire lifetime.
Each entity gets its own Workflow instance handling all state transitions through Signals and Updates.

### [Continue-As-New](continue-as-new.md)

Prevents unbounded history growth by starting a new execution with fresh history.

### [Updatable Timer](updatable-timer.md)

Dynamically adjustable timers that respond to Signals or Updates.
Extend, shorten, or cancel timers based on external events.

## Workflow messaging patterns

### [Signal with Start](signal-with-start.md)

Starts a Workflow when Signaling it if it does not already exist.
If already running, it receives the Signal directly.

### [Request-Response via Updates](request-response-via-updates.md)

Synchronous state modification with validation and direct result return.

## Task orchestration patterns

### [Child Workflows](child-workflows.md)

Decomposes complex Workflows into smaller, reusable Workflow units.
Each child has an independent Workflow ID, history, and lifecycle with flexible parent-child coordination.

### [Parallel Execution](parallel-execution.md)

Executes multiple Activities concurrently for maximum throughput.

### [Pick First (Race)](pick-first.md)

Starts multiple Activities in parallel and uses the first result.

## External interaction patterns

### [Polling External Services](polling.md)

Strategies for polling external resources with varying frequencies.

### [Long-running Activity](long-running-activity.md)

Long-running Activities report progress via heartbeats and enable resumption after failures.

### [Approval](approval.md)

Human-in-the-loop Workflows that block until external approval decisions are made.

### [Delayed Start](delayed-start.md)

Creates Workflows immediately but defers execution until a specified delay expires.

## Worker configuration patterns

### [Worker-Specific Task Queues](worker-specific-taskqueue.md)

Routes Activities to specific Workers using unique Task Queues for Worker affinity.

### [Activity Dependency Injection](activity-dependency-injection.md)

Injects external dependencies (database connections, API clients) into Activities at Worker startup.
Keeps Workflow code deterministic and makes Activities testable with mock implementations.
