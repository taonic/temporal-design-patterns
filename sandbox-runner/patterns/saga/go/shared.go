package main

const (
	TaskQueue        = "saga-task-queue"
	WorkflowIDPrefix = "transfer"
)

type TransferDetails struct {
	TransferID  string `json:"transferId"`
	FromAccount string `json:"fromAccount"`
	ToAccount   string `json:"toAccount"`
	Amount      int    `json:"amount"`
}
