# Cancellation Propagation — TypeScript sample

A runnable demo of the [Cancellation Propagation](https://taonic.github.io/temporal-design-patterns/cancellation-propagation) pattern.

A parent Workflow starts three Child Workflows concurrently inside a cancellation scope — one per fulfillment step (`reserve-inventory`, `authorize-payment`, `book-shipping`). Each child applies its step, then holds the reservation open in a long-running, heartbeating activity. When the starter sends a `stop` signal, the parent cancels the scope, and the cancellation propagates to every child and into its running activity. Each child's reservation activity is cancelled, the child compensates in a non-cancellable scope, and the child ends in a `Canceled` state — while the parent completes normally.

This shows why cancellation is preferable to termination: every child runs its cleanup before it stops.

## Files

| File | Role |
| :--- | :--- |
| `shared.ts` | Task queue name and the list of fulfillment steps |
| `activities.ts` | `applyStep`, `holdReservation` (heartbeating), and `compensateStep` |
| `workflows.ts` | `fulfillOrderWorkflow` (parent) and `fulfillmentStep` (child) |
| `worker.ts` | Registers the Workflows and activities on the task queue |
| `starter.ts` | Starts the Workflow, waits, then sends the `stop` signal |

## Prerequisites

- [Node.js](https://nodejs.org/) 18 or later.
- The [Temporal CLI](https://docs.temporal.io/cli#install), which bundles a local development server.

## Run it

Open three terminals in this directory.

**1. Start a local Temporal development server:**

```bash
temporal server start-dev
```

This serves the gRPC endpoint on `localhost:7233` and the Web UI on [http://localhost:8233](http://localhost:8233).

**2. Install dependencies and start the Worker:**

```bash
npm install
npx tsx worker.ts
```

The Worker prints `Worker listening on task queue 'cancellation-propagation-task-queue'` and waits for tasks.

**3. Run the starter:**

```bash
npx tsx starter.ts
```

## Expected output

The starter prints:

```
Started workflow: cancellation-propagation-<timestamp>
Fulfilling order-42; children are reserving resources concurrently…
Requesting stop; cancellation will propagate to every child…
Order order-42 stopped: cancelled and compensated 3 fulfillment steps (reserve-inventory, authorize-payment, book-shipping)
Open the Temporal UI and search for 'cancellation-propagation-<timestamp>' to see each child transition to Canceled after compensating.
```

The Worker terminal shows the cancellation flow for each step, in order:

```
Applied reserve-inventory for order order-42
Holding reserve-inventory for order order-42
Reservation for reserve-inventory released on cancellation
Compensated reserve-inventory for order order-42
```

In the Web UI, the parent Workflow ends as **Completed**, and each of the three child Workflows ends as **Canceled** after running its compensation.
