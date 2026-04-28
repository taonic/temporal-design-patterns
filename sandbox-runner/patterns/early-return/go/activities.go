package main

import (
	"context"
	"errors"
	"fmt"
	"time"
)

func InitTransaction(_ context.Context, req TransactionRequest) (*Transaction, error) {
	fmt.Printf("Init: validating %.2f %s\n", req.Amount, req.Currency)
	if req.Amount <= 0 {
		return nil, errors.New("invalid amount")
	}
	return &Transaction{
		ID:     fmt.Sprintf("tx-%d", time.Now().UnixMilli()),
		Status: "initialized",
	}, nil
}

func CompleteTransaction(_ context.Context, tx *Transaction) error {
	// Simulate slow background settlement so the early-return effect is visible.
	time.Sleep(2 * time.Second)
	fmt.Printf("Completed transaction %s\n", tx.ID)
	return nil
}

func CancelTransaction(_ context.Context, tx *Transaction) error {
	id := "(uninitialized)"
	if tx != nil {
		id = tx.ID
	}
	fmt.Printf("Cancelled transaction %s\n", id)
	return nil
}
