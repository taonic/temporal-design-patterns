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

	transferID := fmt.Sprintf("%s-%d", WorkflowIDPrefix, time.Now().UnixMilli())
	details := TransferDetails{
		TransferID:  transferID,
		FromAccount: "alice",
		ToAccount:   "bob",
		Amount:      100,
	}

	we, err := c.ExecuteWorkflow(
		context.Background(),
		client.StartWorkflowOptions{
			ID:        transferID,
			TaskQueue: TaskQueue,
		},
		TransferMoneyWorkflow,
		details,
	)
	if err != nil {
		log.Fatalln("Unable to execute workflow:", err)
	}
	fmt.Printf("Started workflow: %s\n", we.GetID())

	var result string
	if err := we.Get(context.Background(), &result); err != nil {
		log.Fatalln("Workflow failed:", err)
	}
	fmt.Println(result)
	fmt.Printf("Open the Temporal UI and search for '%s' to see the saga history.\n", transferID)
}
