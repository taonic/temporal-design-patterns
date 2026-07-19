package main

import (
	"fmt"
	"time"

	"go.temporal.io/sdk/temporal"
	"go.temporal.io/sdk/workflow"
)

// FulfillmentStep is the child workflow: it applies one fulfillment step, holds
// it until the context is cancelled, and compensates on cancellation.
func FulfillmentStep(ctx workflow.Context, orderID, step string) error {
	ao := workflow.ActivityOptions{StartToCloseTimeout: 10 * time.Second}
	ctx = workflow.WithActivityOptions(ctx, ao)

	if err := workflow.ExecuteActivity(ctx, ApplyStep, orderID, step).Get(ctx, nil); err != nil {
		return err
	}

	// Hold the reservation open in a long-running, heartbeating activity until
	// the context is cancelled. WaitForCancellation makes Get block until the
	// activity acknowledges the cancellation and runs its own cleanup.
	holdCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
		StartToCloseTimeout: 5 * time.Minute,
		HeartbeatTimeout:    2 * time.Second,
		WaitForCancellation: true,
	})
	err := workflow.ExecuteActivity(holdCtx, HoldReservation, orderID, step).Get(holdCtx, nil)
	if temporal.IsCanceledError(err) {
		// Compensate on a disconnected context; the original ctx is already cancelled.
		dctx, cancel := workflow.NewDisconnectedContext(ctx)
		defer cancel()
		dctx = workflow.WithActivityOptions(dctx, ao)
		_ = workflow.ExecuteActivity(dctx, CompensateStep, orderID, step).Get(dctx, nil)
		return err // Re-raise so the child reports Canceled.
	}
	return err
}

// FulfillOrderWorkflow is the parent workflow: it starts one child per step with
// a shared cancellable context and cancels the whole group on a stop signal.
func FulfillOrderWorkflow(ctx workflow.Context, orderID string) (string, error) {
	parentID := workflow.GetInfo(ctx).WorkflowExecution.ID

	// Shared cancellable context that every child is started with.
	childCtx, cancel := workflow.WithCancel(ctx)
	defer cancel()

	// A scope owns any mix of operations. Alongside the children, start a timer
	// on the same cancellable context that would fire a follow-up reminder
	// later. Cancelling the context cancels this pending timer as well.
	reminderTimer := workflow.NewTimer(childCtx, time.Hour)

	var futures []workflow.ChildWorkflowFuture
	for _, step := range Steps {
		opts := workflow.ChildWorkflowOptions{
			WorkflowID:          fmt.Sprintf("%s/%s", parentID, step),
			TaskQueue:           TaskQueue,
			WaitForCancellation: true,
		}
		cctx := workflow.WithChildOptions(childCtx, opts)
		futures = append(futures, workflow.ExecuteChildWorkflow(cctx, FulfillmentStep, orderID, step))
	}

	// Cancel every child as soon as a stop signal arrives.
	workflow.Go(ctx, func(gctx workflow.Context) {
		workflow.GetSignalChannel(gctx, "stop").Receive(gctx, nil)
		cancel()
	})

	// Wait for every child; a cancelled child returns a CanceledError.
	for _, f := range futures {
		if err := f.Get(ctx, nil); err != nil && !temporal.IsCanceledError(err) {
			return "", err
		}
	}

	// The timer created on the cancellable context is cancelled along with the
	// children; its future returns a CanceledError.
	reminderCancelled := false
	if err := reminderTimer.Get(ctx, nil); temporal.IsCanceledError(err) {
		reminderCancelled = true
		workflow.GetLogger(ctx).Info("Reminder timer cancelled with the scope", "orderID", orderID)
	}

	result := fmt.Sprintf(
		"Order %s stopped: cancelled and compensated %d fulfillment steps (%v)",
		orderID, len(Steps), Steps,
	)
	if reminderCancelled {
		result += " and cancelled the pending reminder timer"
	}
	return result, nil
}
