// Stub program compiled at image-build time so the Temporal Go SDK and its
// transitive deps land in the Go build cache before any user code runs. The
// runtime `go run` then only has to compile the small main package.
//
// The image factory copies this into the snapshot, runs `go build`, then
// deletes the source — so this file is never present alongside the user's
// worker.go/starter.go at runtime, and the `go run worker.go ...` invocations
// never see it.
//
// NB: do NOT prefix the filename with `_`. Go's package loader filters
// leading-underscore files even when listed explicitly on the command line,
// which manifests as "no Go files in /opt/app" during the warmup build.

package main

import (
	_ "go.temporal.io/sdk/activity"
	_ "go.temporal.io/sdk/client"
	_ "go.temporal.io/sdk/worker"
	_ "go.temporal.io/sdk/workflow"
)

func main() {}
