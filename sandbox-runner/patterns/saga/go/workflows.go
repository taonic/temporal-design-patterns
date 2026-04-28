package main

import (
	"fmt"
	"time"

	"go.temporal.io/sdk/temporal"
	"go.temporal.io/sdk/workflow"
)

// TransferMoneyWorkflow demonstrates the Saga pattern with a slice of
// compensation closures. On any step failure we run them in reverse order
// and return a status string instead of propagating the error — so the
// workflow execution itself succeeds and the result string carries the
// rollback reason. (See saga-pattern.md for the canonical re-throw variant.)
func TransferMoneyWorkflow(ctx workflow.Context, details TransferDetails) (string, error) {
	ao := workflow.ActivityOptions{
		StartToCloseTimeout: 10 * time.Second,
		RetryPolicy:         &temporal.RetryPolicy{MaximumAttempts: 1},
	}
	ctx = workflow.WithActivityOptions(ctx, ao)

	logger := workflow.GetLogger(ctx)
	logger.Info("Starting transfer", "id", details.TransferID, "amount", details.Amount)

	var compensations []func()
	rollback := func(err error) string {
		logger.Warn("Transfer failed, running compensations",
			"id", details.TransferID, "err", err, "count", len(compensations))
		for i := len(compensations) - 1; i >= 0; i-- {
			compensations[i]()
		}
		return fmt.Sprintf("Transfer %s rolled back: %v", details.TransferID, err)
	}

	compensations = append(compensations, func() {
		if compErr := workflow.ExecuteActivity(ctx, WithdrawCompensation, details).Get(ctx, nil); compErr != nil {
			logger.Error("Withdraw compensation failed", "err", compErr)
		}
	})
	if err := workflow.ExecuteActivity(ctx, Withdraw, details).Get(ctx, nil); err != nil {
		return rollback(err), nil
	}

	compensations = append(compensations, func() {
		if compErr := workflow.ExecuteActivity(ctx, DepositCompensation, details).Get(ctx, nil); compErr != nil {
			logger.Error("Deposit compensation failed", "err", compErr)
		}
	})
	if err := workflow.ExecuteActivity(ctx, Deposit, details).Get(ctx, nil); err != nil {
		return rollback(err), nil
	}

	if err := workflow.ExecuteActivity(ctx, NotifyDownstream, details).Get(ctx, nil); err != nil {
		return rollback(err), nil
	}

	return fmt.Sprintf("Transfer %s completed", details.TransferID), nil
}
