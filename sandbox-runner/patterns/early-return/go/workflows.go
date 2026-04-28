package main

import (
	"time"

	"go.temporal.io/sdk/workflow"
)

// TransactionWorkflow demonstrates the Early Return pattern. An Update handler
// blocks on `initDone` and returns the initialization result to the caller as
// soon as Phase 1 finishes; the workflow itself keeps running and executes the
// slow Phase 2 (completion or cancellation) in the background.
func TransactionWorkflow(ctx workflow.Context, req TransactionRequest) (*Transaction, error) {
	var tx *Transaction
	var initDone bool
	var initErr error

	err := workflow.SetUpdateHandler(ctx, UpdateName,
		func(ctx workflow.Context) (*Transaction, error) {
			workflow.Await(ctx, func() bool { return initDone })
			return tx, initErr
		},
	)
	if err != nil {
		return nil, err
	}

	// Phase 1: fast synchronous initialization (local activity).
	localCtx := workflow.WithLocalActivityOptions(ctx, workflow.LocalActivityOptions{
		ScheduleToCloseTimeout: 5 * time.Second,
	})
	initErr = workflow.ExecuteLocalActivity(localCtx, InitTransaction, req).Get(localCtx, &tx)
	initDone = true

	// Phase 2: slow asynchronous completion.
	activityCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
		StartToCloseTimeout: 30 * time.Second,
	})

	if initErr != nil {
		return nil, workflow.ExecuteActivity(activityCtx, CancelTransaction, tx).Get(activityCtx, nil)
	}

	return tx, workflow.ExecuteActivity(activityCtx, CompleteTransaction, tx).Get(activityCtx, nil)
}
