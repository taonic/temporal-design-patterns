package main

import (
	"context"
	"errors"
	"fmt"
)

func Withdraw(_ context.Context, d TransferDetails) error {
	fmt.Printf("Withdrew $%d from %s\n", d.Amount, d.FromAccount)
	return nil
}

func Deposit(_ context.Context, d TransferDetails) error {
	fmt.Printf("Deposited $%d to %s\n", d.Amount, d.ToAccount)
	return nil
}

func NotifyDownstream(_ context.Context, d TransferDetails) error {
	fmt.Printf("Notify: simulating downstream failure for transfer %s\n", d.TransferID)
	// Replace with `return nil` to watch the saga succeed end-to-end:
	return errors.New("notification service down")
}

func WithdrawCompensation(_ context.Context, d TransferDetails) error {
	fmt.Printf("Refunded $%d to %s\n", d.Amount, d.FromAccount)
	return nil
}

func DepositCompensation(_ context.Context, d TransferDetails) error {
	fmt.Printf("Reversed deposit of $%d from %s\n", d.Amount, d.ToAccount)
	return nil
}
