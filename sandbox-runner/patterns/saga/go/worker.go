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

	w := worker.New(c, TaskQueue, worker.Options{})
	w.RegisterWorkflow(OpenAccountWorkflow)
	w.RegisterActivity(CreateAccount)
	w.RegisterActivity(AddAddress)
	w.RegisterActivity(AddClient)
	w.RegisterActivity(AddBankAccount)
	w.RegisterActivity(ClearPostalAddresses)
	w.RegisterActivity(RemoveClient)
	w.RegisterActivity(DisconnectBankAccounts)

	log.Printf("Worker listening on task queue '%s'", TaskQueue)
	if err := w.Run(worker.InterruptCh()); err != nil {
		log.Fatalln("Worker run failed:", err)
	}
}
