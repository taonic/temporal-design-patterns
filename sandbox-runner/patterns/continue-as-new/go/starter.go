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

	workflowID := fmt.Sprintf("%s-%d", WorkflowIDPrefix, time.Now().UnixMilli())
	we, err := c.ExecuteWorkflow(
		context.Background(),
		client.StartWorkflowOptions{
			ID:        workflowID,
			TaskQueue: TaskQueue,
		},
		DataProcessorWorkflow,
		"",
		0,
	)
	if err != nil {
		log.Fatalln("Unable to execute workflow:", err)
	}
	fmt.Printf("Started workflow: %s\n", we.GetID())

	var total int
	if err := we.Get(context.Background(), &total); err != nil {
		log.Fatalln("Workflow failed:", err)
	}
	fmt.Printf("Final result: processed %d records\n", total)
	fmt.Printf("Open the Temporal UI and search for '%s' to see the Continue-As-New chain.\n", workflowID)
}
