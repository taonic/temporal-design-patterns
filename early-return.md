### Two-Phase Operations (Early Return)

[Go Sample](https://github.com/temporalio/samples-go/tree/main/early-return)  
[Java Sample](https://github.com/temporalio/samples-java/tree/main/core/src/main/java/io/temporal/samples/earlyreturn)

#### Intent
Return initialization results to the caller immediately while continuing asynchronous processing in the background.

#### Problem
Clients need immediate feedback on whether an operation can proceed, but the full operation takes significant time to complete. Blocking the client for the entire operation duration creates poor user experience and ties up resources.

#### Solution
Uses Update-with-Start to split operations into two phases: a fast synchronous initialization phase that validates and returns results immediately, and a slower asynchronous completion phase that runs in the background. The workflow uses local activities for quick initialization, signals completion via update handlers, then either completes or cancels the operation based on initialization success.

**Go Implementation:**
```go
func Workflow(ctx workflow.Context, txRequest TransactionRequest) (*Transaction, error) {
    var tx *Transaction
    var initDone bool
    var initErr error

    // Register update handler that waits for initialization
    workflow.SetUpdateHandler(ctx, UpdateName,
        func(ctx workflow.Context) (*Transaction, error) {
            workflow.Await(ctx, func() bool { return initDone })
            return tx, initErr
        },
    )

    // Phase 1: Fast synchronous initialization (local activity)
    localOpts := workflow.WithLocalActivityOptions(ctx, workflow.LocalActivityOptions{
        ScheduleToCloseTimeout: 5 * time.Second,
    })
    initErr = workflow.ExecuteLocalActivity(localOpts, txRequest.Init).Get(ctx, &tx)
    initDone = true // Signal update handler

    // Phase 2: Slow asynchronous completion
    activityCtx := workflow.WithActivityOptions(ctx, workflow.ActivityOptions{
        StartToCloseTimeout: 30 * time.Second,
    })

    if initErr != nil {
        // Cancel on initialization failure
        return nil, workflow.ExecuteActivity(activityCtx, CancelTransaction, tx).Get(ctx, nil)
    }

    // Complete on initialization success
    return tx, workflow.ExecuteActivity(activityCtx, CompleteTransaction, tx).Get(ctx, nil)
}
```

**Java Implementation:**
```java
public class TransactionWorkflowImpl implements TransactionWorkflow {
    private boolean initDone = false;
    private Transaction tx;
    private Exception initError = null;

    @Override
    public TxResult processTransaction(TransactionRequest txRequest) {
        this.tx = activities.mintTransactionId(txRequest);

        // Phase 1: Fast synchronous initialization
        try {
            this.tx = activities.initTransaction(this.tx);
        } catch (Exception e) {
            initError = e;
        } finally {
            initDone = true; // Signal update handler
        }

        // Phase 2: Slow asynchronous completion
        if (initError != null) {
            activities.cancelTransaction(this.tx);
            return new TxResult("", "Transaction cancelled.");
        } else {
            activities.completeTransaction(this.tx);
            return new TxResult(this.tx.getId(), "Transaction completed successfully.");
        }
    }

    @Override
    public TxResult returnInitResult() {
        Workflow.await(() -> initDone); // Wait for initialization
        if (initError != null) {
            throw Workflow.wrap(initError);
        }
        return new TxResult(tx.getId(), "Initialization successful");
    }
}
```

**Key Differences:**
- **Go**: Uses SetUpdateHandler with closure capturing variables
- **Java**: Uses separate update method (returnInitResult) with instance variables
- **Both**: Use Workflow.await() to block until initialization completes
- **Both**: Return initialization result immediately while processing continues

#### Applicability
Use this pattern when:
- Clients need immediate feedback but operations take time to complete
- Validation or initialization can be done quickly (< 5 seconds)
- The operation can be safely cancelled if initialization fails
- You want to avoid blocking clients during long-running processing
- The initialization result determines whether to proceed or abort

#### Pros
- ✅ Immediate client feedback via Update-with-Start in single round trip
- ✅ Non-blocking - clients don't wait for full operation completion
- ✅ Local activities avoid extra server roundtrips during initialization
- ✅ Clear separation between validation and execution phases
- ✅ Automatic cancellation handling on initialization failure

#### Cons
- ❌ Requires careful timeout tuning for local activities
- ❌ Clients must handle asynchronous completion separately
- ❌ More complex than simple synchronous workflows
- ❌ Initialization must complete within a single workflow task
- ❌ Limited to operations that can be split into fast/slow phases

#### Relations with Other Patterns
- Uses **Local Activities** for fast initialization without server roundtrips
- Can combine with **Saga Pattern** to add compensation for failed completions
- Often paired with **Signals** or **Queries** for clients to check completion status
- May use **Async Activity Completion** for external system integration in phase 2
