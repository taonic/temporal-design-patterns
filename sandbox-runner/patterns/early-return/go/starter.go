package main

import (
	"context"
	"fmt"
	"log"
	"time"

	enumspb "go.temporal.io/api/enums/v1"
	"go.temporal.io/sdk/client"
)

func main() {
	c, err := client.Dial(client.Options{HostPort: "localhost:7233"})
	if err != nil {
		log.Fatalln("Unable to create client:", err)
	}
	defer c.Close()

	ctx := context.Background()
	transactionID := fmt.Sprintf("%s-%d", WorkflowIDPrefix, time.Now().UnixMilli())
	req := TransactionRequest{Amount: 100, Currency: "USD"}

	startOp := c.NewWithStartWorkflowOperation(
		client.StartWorkflowOptions{
			ID:                       transactionID,
			TaskQueue:                TaskQueue,
			WorkflowIDConflictPolicy: enumspb.WORKFLOW_ID_CONFLICT_POLICY_FAIL,
		},
		TransactionWorkflow,
		req,
	)

	t0 := time.Now()
	updateHandle, err := c.UpdateWithStartWorkflow(ctx, client.UpdateWithStartWorkflowOptions{
		StartWorkflowOperation: startOp,
		UpdateOptions: client.UpdateWorkflowOptions{
			UpdateName:   UpdateName,
			WaitForStage: client.WorkflowUpdateStageCompleted,
		},
	})
	if err != nil {
		log.Fatalln("UpdateWithStartWorkflow failed:", err)
	}

	var tx Transaction
	if err := updateHandle.Get(ctx, &tx); err != nil {
		log.Fatalln("Update result failed:", err)
	}
	fmt.Printf("Early return after %dms: %s (status=%s)\n",
		time.Since(t0).Milliseconds(), tx.ID, tx.Status)

	we, err := startOp.Get(ctx)
	if err != nil {
		log.Fatalln("Workflow start failed:", err)
	}
	var final Transaction
	if err := we.Get(ctx, &final); err != nil {
		log.Fatalln("Workflow result failed:", err)
	}
	fmt.Printf("Workflow completed after %dms: %s (status=%s)\n",
		time.Since(t0).Milliseconds(), final.ID, final.Status)
	fmt.Printf("Open the Temporal UI and search for '%s' to see the history.\n", transactionID)
}
