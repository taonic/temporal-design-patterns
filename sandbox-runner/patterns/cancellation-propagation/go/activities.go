package main

import (
	"context"
	"time"

	"go.temporal.io/sdk/activity"
)

// ApplyStep reserves a resource for one fulfillment step.
func ApplyStep(ctx context.Context, orderID, step string) error {
	activity.GetLogger(ctx).Info("Applied step", "order", orderID, "step", step)
	// Simulate holding a real reservation.
	time.Sleep(100 * time.Millisecond)
	return nil
}

// HoldReservation is a long-running activity that keeps the reservation open
// until it is cancelled. It heartbeats on each iteration so the server can
// deliver the cancellation request, then returns once the context is cancelled.
func HoldReservation(ctx context.Context, orderID, step string) error {
	logger := activity.GetLogger(ctx)
	logger.Info("Holding step", "order", orderID, "step", step)
	for {
		select {
		case <-ctx.Done():
			logger.Info("Reservation released on cancellation", "order", orderID, "step", step)
			return ctx.Err()
		case <-time.After(1 * time.Second):
			activity.RecordHeartbeat(ctx, step)
		}
	}
}

// CompensateStep undoes a previously applied fulfillment step.
func CompensateStep(ctx context.Context, orderID, step string) error {
	activity.GetLogger(ctx).Info("Compensated step", "order", orderID, "step", step)
	time.Sleep(100 * time.Millisecond)
	return nil
}
