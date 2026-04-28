package main

import (
	"context"
	"errors"
	"fmt"
)

func CreateAccount(_ context.Context, req OpenAccountRequest) error {
	fmt.Printf("Created account %s for %s\n", req.AccountID, req.ClientName)
	return nil
}

func AddAddress(_ context.Context, req OpenAccountRequest) error {
	fmt.Printf("Added address '%s' to %s\n", req.Address, req.AccountID)
	return nil
}

func AddClient(_ context.Context, req OpenAccountRequest) error {
	fmt.Printf("Added client %s to %s\n", req.ClientEmail, req.AccountID)
	return nil
}

func AddBankAccount(_ context.Context, req OpenAccountRequest) error {
	fmt.Printf("Linking bank account %s: simulating downstream failure\n", req.BankAccount)
	// Replace with `return nil` to watch the saga succeed end-to-end:
	return errors.New("bank link service down")
}

func ClearPostalAddresses(_ context.Context, req OpenAccountRequest) error {
	fmt.Printf("Cleared postal addresses for %s\n", req.AccountID)
	return nil
}

func RemoveClient(_ context.Context, req OpenAccountRequest) error {
	fmt.Printf("Removed client from %s\n", req.AccountID)
	return nil
}

func DisconnectBankAccounts(_ context.Context, req OpenAccountRequest) error {
	fmt.Printf("Disconnected any bank accounts from %s\n", req.AccountID)
	return nil
}
