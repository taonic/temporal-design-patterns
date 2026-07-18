package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"go.temporal.io/sdk/client"
)

func main() {
	c, err := client.Dial(client.Options{HostPort: "localhost:7233"})
	if err != nil {
		log.Fatalln("Unable to create client:", err)
	}
	defer c.Close()

	ctx := context.Background()
	workflowID := fmt.Sprintf("%s-%d", WorkflowIDPrefix, time.Now().UnixMilli())
	orderID := "order-42"

	we, err := c.ExecuteWorkflow(ctx, client.StartWorkflowOptions{
		ID:        workflowID,
		TaskQueue: TaskQueue,
	}, FulfillOrderWorkflow, orderID)
	if err != nil {
		log.Fatalln("Unable to execute workflow:", err)
	}
	fmt.Printf("Started workflow: %s\n", we.GetID())
	fmt.Printf("Fulfilling %s; children are reserving resources concurrently…\n", orderID)

	// Let the children apply their steps, then request a stop.
	time.Sleep(2 * time.Second)
	fmt.Println("Requesting stop; cancellation will propagate to every child…")
	if err := c.SignalWorkflow(ctx, workflowID, we.GetRunID(), "stop", nil); err != nil {
		log.Fatalln("Unable to signal workflow:", err)
	}

	var result string
	if err := we.Get(ctx, &result); err != nil {
		log.Fatalln("Workflow failed:", err)
	}
	fmt.Println(result)
	fmt.Printf(
		"Open the Temporal UI and search for '%s' to see each child transition to Canceled after compensating.\n",
		workflowID,
	)
}
