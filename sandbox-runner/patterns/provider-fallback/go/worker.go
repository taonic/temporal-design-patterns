package main

import (
	"log"

	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
)

func main() {
	c, err := client.Dial(client.Options{HostPort: "localhost:7233"})
	if err != nil {
		log.Fatalln("Unable to create client:", err)
	}
	defer c.Close()

	// One registry shared by every Activity this worker runs, injected into the
	// Activities value instead of reached for as a package global. See the note in
	// activities.go on why this is safe only for same-worker, per-Workflow-keyed state.
	activities := &Activities{registry: NewLLMRegistry()}

	w := worker.New(c, TaskQueue, worker.Options{})
	w.RegisterWorkflow(ProviderFallbackWorkflow)
	w.RegisterActivity(activities)

	log.Printf("Worker listening on task queue '%s'", TaskQueue)
	if err := w.Run(worker.InterruptCh()); err != nil {
		log.Fatalln("Worker run failed:", err)
	}
}
