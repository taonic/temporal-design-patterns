package main

import (
	"time"

	"go.temporal.io/sdk/workflow"
)

func DataProcessorWorkflow(ctx workflow.Context, cursor string, totalProcessed int) (int, error) {
	ao := workflow.ActivityOptions{StartToCloseTimeout: 10 * time.Second}
	ctx = workflow.WithActivityOptions(ctx, ao)

	var batch []Record
	if err := workflow.ExecuteActivity(ctx, FetchBatch, cursor, BatchSize).Get(ctx, &batch); err != nil {
		return totalProcessed, err
	}

	for _, record := range batch {
		if err := workflow.ExecuteActivity(ctx, ProcessRecord, record).Get(ctx, nil); err != nil {
			return totalProcessed, err
		}
		totalProcessed++
		cursor = record.ID
	}

	workflow.GetLogger(ctx).Info("Processed batch", "size", len(batch), "total", totalProcessed)

	if len(batch) == BatchSize {
		return totalProcessed, workflow.NewContinueAsNewError(ctx, DataProcessorWorkflow, cursor, totalProcessed)
	}
	return totalProcessed, nil
}
