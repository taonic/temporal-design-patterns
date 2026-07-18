# Cancellation Propagation — Go sample

A runnable demo of the [Cancellation Propagation](https://taonic.github.io/temporal-design-patterns/cancellation-propagation) pattern.

A parent Workflow starts three Child Workflows concurrently with a shared cancellable context — one per fulfillment step (`reserve-inventory`, `authorize-payment`, `book-shipping`). Each child applies its step, then holds the reservation open in a long-running, heartbeating activity. When the starter sends a `stop` signal, the parent calls the context's cancel function, and the cancellation propagates to every child and into its running activity. Each child's reservation activity is cancelled, the child compensates on a disconnected context, and the child ends in a `Canceled` state — while the parent completes normally.

This shows why cancellation is preferable to termination: every child runs its cleanup before it stops.

## Files

| File | Role |
| :--- | :--- |
| `shared.go` | Task queue name and the list of fulfillment steps |
| `activities.go` | `ApplyStep`, `HoldReservation` (heartbeating), and `CompensateStep` |
| `workflows.go` | `FulfillOrderWorkflow` (parent) and `FulfillmentStep` (child) |
| `worker.go` | Registers the Workflows and activities on the task queue |
| `starter.go` | Starts the Workflow, waits, then sends the `stop` signal |

## Prerequisites

- [Go](https://go.dev/dl/) 1.22 or later.
- The [Temporal CLI](https://docs.temporal.io/cli#install), which bundles a local development server.

## Run it

Open three terminals in this directory.

**1. Start a local Temporal development server:**

```bash
temporal server start-dev
```

This serves the gRPC endpoint on `localhost:7233` and the Web UI on [http://localhost:8233](http://localhost:8233).

**2. Start the Worker:**

```bash
go run worker.go workflows.go activities.go shared.go
```

The Worker prints `Worker listening on task queue 'cancellation-propagation-task-queue'` and waits for tasks.

**3. Run the starter:**

```bash
go run starter.go workflows.go activities.go shared.go
```

## Expected output

The starter prints:

```
Started workflow: cancellation-propagation-<timestamp>
Fulfilling order-42; children are reserving resources concurrently…
Requesting stop; cancellation will propagate to every child…
Order order-42 stopped: cancelled and compensated 3 fulfillment steps ([reserve-inventory authorize-payment book-shipping])
Open the Temporal UI and search for 'cancellation-propagation-<timestamp>' to see each child transition to Canceled after compensating.
```

The Worker terminal logs the cancellation flow for each step: `Applied step` → `Holding step` → `Reservation released on cancellation` → `Compensated step`.

In the Web UI, the parent Workflow ends as **Completed**, and each of the three child Workflows ends as **Canceled** after running its compensation.
