package main

import (
	"fmt"
	"time"

	"go.temporal.io/sdk/temporal"
	"go.temporal.io/sdk/workflow"
)

// OpenAccountWorkflow demonstrates the Saga pattern with a slice of
// compensation closures. On any step failure we run them in reverse order
// and return a status string instead of propagating the error — so the
// workflow execution itself succeeds and the result string carries the
// rollback reason. (See saga-pattern.md for the canonical re-throw variant.)
func OpenAccountWorkflow(ctx workflow.Context, req OpenAccountRequest) (string, error) {
	ao := workflow.ActivityOptions{
		StartToCloseTimeout: 10 * time.Second,
		RetryPolicy:         &temporal.RetryPolicy{MaximumAttempts: 1},
	}
	ctx = workflow.WithActivityOptions(ctx, ao)

	logger := workflow.GetLogger(ctx)
	logger.Info("Opening account", "id", req.AccountID, "client", req.ClientName)

	var compensations []func()
	rollback := func(err error) string {
		logger.Warn("Open account failed, running compensations",
			"id", req.AccountID, "err", err, "count", len(compensations))
		for i := len(compensations) - 1; i >= 0; i-- {
			compensations[i]()
		}
		return fmt.Sprintf("Account %s rolled back: %v", req.AccountID, err)
	}

	// Step 1: CreateAccount has no compensation — leaving an empty account
	// stub on later failure is acceptable for this demo.
	if err := workflow.ExecuteActivity(ctx, CreateAccount, req).Get(ctx, nil); err != nil {
		return rollback(err), nil
	}

	compensations = append(compensations, func() {
		if compErr := workflow.ExecuteActivity(ctx, ClearPostalAddresses, req).Get(ctx, nil); compErr != nil {
			logger.Error("ClearPostalAddresses compensation failed", "err", compErr)
		}
	})
	if err := workflow.ExecuteActivity(ctx, AddAddress, req).Get(ctx, nil); err != nil {
		return rollback(err), nil
	}

	compensations = append(compensations, func() {
		if compErr := workflow.ExecuteActivity(ctx, RemoveClient, req).Get(ctx, nil); compErr != nil {
			logger.Error("RemoveClient compensation failed", "err", compErr)
		}
	})
	if err := workflow.ExecuteActivity(ctx, AddClient, req).Get(ctx, nil); err != nil {
		return rollback(err), nil
	}

	compensations = append(compensations, func() {
		if compErr := workflow.ExecuteActivity(ctx, DisconnectBankAccounts, req).Get(ctx, nil); compErr != nil {
			logger.Error("DisconnectBankAccounts compensation failed", "err", compErr)
		}
	})
	if err := workflow.ExecuteActivity(ctx, AddBankAccount, req).Get(ctx, nil); err != nil {
		return rollback(err), nil
	}

	return fmt.Sprintf("Account %s opened", req.AccountID), nil
}
