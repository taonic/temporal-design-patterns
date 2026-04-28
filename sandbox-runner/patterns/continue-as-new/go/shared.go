package main

const (
	TaskQueue        = "continue-as-new-task-queue"
	WorkflowIDPrefix = "data-processor"
	BatchSize        = 10
	TotalRecords     = 20
)

type Record struct {
	ID string `json:"id"`
}
