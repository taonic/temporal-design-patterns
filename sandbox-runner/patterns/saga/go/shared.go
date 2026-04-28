package main

const (
	TaskQueue        = "saga-task-queue"
	WorkflowIDPrefix = "open-account"
)

type OpenAccountRequest struct {
	AccountID   string `json:"accountId"`
	ClientName  string `json:"clientName"`
	ClientEmail string `json:"clientEmail"`
	Address     string `json:"address"`
	BankAccount string `json:"bankAccount"`
}
