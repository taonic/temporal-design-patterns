package main

const (
	TaskQueue        = "early-return-task-queue"
	WorkflowIDPrefix = "transaction"
	UpdateName       = "returnInitResult"
)

type TransactionRequest struct {
	Amount   float64 `json:"amount"`
	Currency string  `json:"currency"`
}

type Transaction struct {
	ID     string `json:"id"`
	Status string `json:"status"`
}
