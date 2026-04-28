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

	accountID := fmt.Sprintf("%s-%d", WorkflowIDPrefix, time.Now().UnixMilli())
	req := OpenAccountRequest{
		AccountID:   accountID,
		ClientName:  "Alice Example",
		ClientEmail: "alice@example.com",
		Address:     "123 Main St, Brooklyn NY",
		BankAccount: "DE89-3704-0044-0532-0130-00",
	}

	we, err := c.ExecuteWorkflow(
		context.Background(),
		client.StartWorkflowOptions{
			ID:        accountID,
			TaskQueue: TaskQueue,
		},
		OpenAccountWorkflow,
		req,
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
	fmt.Printf("Open the Temporal UI and search for '%s' to see the saga history.\n", accountID)
}
