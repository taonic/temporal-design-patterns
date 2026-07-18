package main

const (
	TaskQueue        = "cancellation-propagation-task-queue"
	WorkflowIDPrefix = "cancellation-propagation"
)

// Steps is the set of fulfillment steps run concurrently as child workflows.
var Steps = []string{"reserve-inventory", "authorize-payment", "book-shipping"}
