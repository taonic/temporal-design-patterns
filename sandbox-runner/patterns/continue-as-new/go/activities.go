package main

import (
	"context"
	"strconv"
	"time"
)

func FetchBatch(_ context.Context, cursor string, batchSize int) ([]Record, error) {
	start := 0
	if cursor != "" {
		n, err := strconv.Atoi(cursor)
		if err != nil {
			return nil, err
		}
		start = n + 1
	}
	end := start + batchSize
	if end > TotalRecords {
		end = TotalRecords
	}
	out := make([]Record, 0, end-start)
	for i := start; i < end; i++ {
		out = append(out, Record{ID: strconv.Itoa(i)})
	}
	return out, nil
}

func ProcessRecord(_ context.Context, _ Record) error {
	time.Sleep(50 * time.Millisecond)
	return nil
}
