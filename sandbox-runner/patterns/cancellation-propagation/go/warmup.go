// Stub program compiled at image-build time so the Temporal Go SDK and its
// transitive deps land in the Go build cache before any user code runs.
// The image factory deletes this file after building.
package main

import (
	_ "go.temporal.io/sdk/activity"
	_ "go.temporal.io/sdk/client"
	_ "go.temporal.io/sdk/worker"
	_ "go.temporal.io/sdk/workflow"
)

func main() {}
